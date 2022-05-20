from django.db import models
from django.conf import settings
from django.utils.html import escape
import re
from django.template.defaultfilters import truncatechars
from authentication.models import Lab
from brain.models import AtlasModel, Animal, BrainRegion
from django_mysql.models import EnumField

class NeuroglancerModel(AtlasModel):
    neuroglancer_state = models.JSONField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, db_column="FK_owner_id",
                               verbose_name="User")
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    user_date = models.CharField(max_length=25)
    comments = models.CharField(max_length=255)
    readonly = models.BooleanField(default=False, db_column='readonly')

    @property
    def short_description(self):
        return truncatechars(self.neuroglancer_state, 50)

    @property
    def escape_state(self):
        return escape(self.neuroglancer_state)

    @property
    def animal(self):
        """
        find the animal within the url between data/ and /neuroglancer_data:
        data/MD589/neuroglancer_data/C1
        return: the first match if found, otherwise NA
        """
        animal = "NA"
        match = re.search('data/(.+?)/neuroglancer_data', str(self.neuroglancer_state))
        if match is not None and match.group(1) is not None:
            animal = match.group(1)
        return animal


    @property
    def layers(self):
        layer_list = []
        if self.neuroglancer_state is not None:
            json_txt = self.neuroglancer_state
            layers = json_txt['layers']
            for layer in layers:
                if 'annotations' in layer:
                    label = layer['name']
                    layer_list.append(label)

        return layer_list
    
    @property
    def lab(self):
        '''
        The primary lab of the user
        :param obj: animal model
        '''
        lab = "NA"
        if self.owner is not None and self.owner.lab is not None:
            lab = self.owner.lab
        return lab


    class Meta:
        managed = True
        verbose_name = "Neuroglancer State"
        verbose_name_plural = "Neuroglancer States"
        ordering = ('comments', 'created')
        db_table = 'neuroglancer_state'

    def __str__(self):
        return u'{}'.format(self.comments)

class NeuroglancerView(AtlasModel):
    group_name = models.CharField(max_length=50, verbose_name='Animal/Structure name')
    lab = models.ForeignKey(Lab, models.CASCADE, null=True, db_column="FK_lab_id", verbose_name='Lab')
    layer_name = models.CharField(max_length=25, blank=False, null=False)
    description = models.TextField(max_length=2001, blank=False, null=False)
    url = models.TextField(max_length=2001, blank=False, null=False)
    thumbnail_url = models.TextField(max_length=2001, blank=False, null=False, verbose_name='Thumbnail name')
    layer_type = EnumField(choices=['image','segmentation'], blank=False, null=False, default='image')
    resolution = models.FloatField(verbose_name="XY Resolution (um)")
    zresolution = models.FloatField(verbose_name="Z Resolution (um)")
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'available_neuroglancer_data'
        verbose_name = 'Available Neuroglancer data'
        verbose_name_plural = 'Available Neuroglancer data'
        ordering = ['lab', 'group_name', 'layer_name']


    def __str__(self):
        return u'{} {}'.format(self.group_name, self.description)

class AnnotationAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, models.CASCADE, null=True, db_column="FK_animal_id", verbose_name="Animal")
    brain_region = models.ForeignKey(BrainRegion, models.CASCADE, null=True, db_column="FK_structure_id",
                               verbose_name="Structure")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column="FK_owner_id",
                               verbose_name="Owner", blank=False, null=False)
    label = models.CharField(max_length=255)
    x = models.FloatField(verbose_name="X (um)")
    y = models.FloatField(verbose_name="Y (um)")
    z = models.FloatField(verbose_name="Z (um)")

    class Meta:
        abstract = True

class ArchiveSet(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    parent =  models.IntegerField(db_column='FK_parent')
    updatedby = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 
                               verbose_name="Updated by", blank=False, null=False, 
                               db_column='FK_update_user_id')
    class Meta:
        managed = True
        db_table = 'archive_set'
        verbose_name = 'Archive set'
        verbose_name_plural = 'Archive sets'

class AnnotationPoints(AnnotationAbstract):

    class Meta:
        managed = True
        db_table = 'annotations_points'
        verbose_name = 'Annotation Point'
        verbose_name_plural = 'Annotation Points'

    def __str__(self):
        return u'{} {}'.format(self.animal, self.label)

class AnnotationPointArchive(AnnotationAbstract):
    archive = models.ForeignKey(ArchiveSet, models.CASCADE, 
                               verbose_name="Archive Set", blank=True, null=True, 
                               db_column='FK_archive_set_id')

    class Meta:
        managed = True
        db_table = 'annotations_point_archive'
        verbose_name = 'Annotation Point Archive'
        verbose_name_plural = 'Annotation Points Archive'
        
class MouselightNeuron(models.Model):
    id = models.BigAutoField(primary_key=True)
    idstring = models.CharField(max_length=64,null=False)
    sample_date = models.DateTimeField(null=True)
    sample_strain = models.CharField(max_length=255,null=True)
    virus_label = models.CharField(max_length=255,null=True) 
    fluorophore_label = models.CharField(max_length=255,null=True)
    annotation_space = models.CharField(
        max_length=20,
        choices=[
            ("ccfv3_25um","Allen Mouse Common Coordinate Framework v3, 25 micron isotropic"),
            ("ccfv3_hierarch_25um","Hierarchical region labeling for Allen Mouse Common Coordinate Framework v3, 25 micron isotropic"),
            ("pma_20um","Princeton Mouse Brain Atlas, 20 micron isotropic"),
            ("pma_hierarch_20um","Hierarchical region labeling for Princeton Mouse Brain Atlas, 20 micron isotropic")
        ],
        default="ccfv3_25um",
    )
    soma_atlas_id = models.PositiveIntegerField(null=True)
    axon_endpoints_dict = models.JSONField(default=dict)
    axon_branches_dict = models.JSONField(default=dict)
    dendrite_endpoints_dict = models.JSONField(default=dict)
    dendrite_branches_dict = models.JSONField(default=dict)

    class Meta:
        managed = True
        verbose_name = "MouseLight Neuron"
        verbose_name_plural = "MouseLight Neurons"
        db_table = 'mouselight_neuron'

    def __str__(self):
        return u'{}'.format(self.idstring)

class ViralTracingLayer(models.Model):
    id = models.BigAutoField(primary_key=True)
    brain_name = models.CharField(max_length=128,null=False)
    virus = models.CharField(max_length=32,null=False)
    timepoint = models.CharField(max_length=32,null=False)
    primary_inj_site = models.CharField(max_length=32,null=True)
    frac_inj_lob_i_v = models.FloatField(null=True) # fraction of injection in Lobules I-V
    frac_inj_lob_vi_vii = models.FloatField(null=True) # fraction of injection in Lobules VI and VII 
    frac_inj_lob_viii_x = models.FloatField(null=True) # fraction of injection in Lobules VIII-X
    frac_inj_simplex = models.FloatField(null=True) # fraction of injection in Simplex
    frac_inj_crusi = models.FloatField(null=True) # fraction of injection in Crus I
    frac_inj_crusii = models.FloatField(null=True) # fraction of injection in Crus II
    frac_inj_pm_cp = models.FloatField(null=True) # fraction of injection in Paramedian lobule and Copula Pyramidis

    class Meta:
        managed = True
        verbose_name = "Tom Pisano Viral Tracing Experiment Brain"
        verbose_name_plural = "Viral Tracing Brain"
        db_table = 'viral_tracing_layer'

    def __str__(self):
        return u'{}'.format(self.brain_name)

