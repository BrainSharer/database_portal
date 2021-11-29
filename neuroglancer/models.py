from django.db import models
from django.conf import settings
from django.utils.html import escape
import re
from enum import Enum
from django.template.defaultfilters import truncatechars
from brain.models import AtlasModel, Animal


class AnnotationChoice(str, Enum):
    POINT = 'point'
    LINE = 'line'

    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    def __str__(self):
        return self.value


class NeuroglancerModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    neuroglancer_state = models.JSONField()
    person = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, db_column="person_id",
                               verbose_name="User")
    # lab = models.ForeignKey(Lab, models.CASCADE, null=True, db_column="lab_id", verbose_name="Lab")
    vetted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    user_date = models.CharField(max_length=25)
    comments = models.CharField(max_length=255)

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
                    layer_name = layer['name']
                    layer_list.append(layer_name)

        return layer_list

    class Meta:
        managed = True
        verbose_name = "Neuroglancer State"
        verbose_name_plural = "Neuroglancer States"
        ordering = ('comments', 'created')
        db_table = 'neuroglancer_state'

    def __str__(self):
        return u'{}'.format(self.comments)


class Structure(AtlasModel):
    id = models.BigAutoField(primary_key=True)
    abbreviation = models.CharField(max_length=200)
    description = models.TextField(max_length=2001, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'structure'
        verbose_name = 'Structure'
        verbose_name_plural = 'Structures'

    def __str__(self):
        return f'{self.description} {self.abbreviation}'


class InputType(models.Model):
    id = models.BigAutoField(primary_key=True)
    input_type = models.CharField(max_length=50, blank=False, null=False, verbose_name='Annotation Type')
    description = models.TextField(max_length=255, blank=False, null=False)
    active = models.BooleanField(default=True, db_column='active')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'input_type'
        verbose_name = 'Annotation Type'
        verbose_name_plural = 'Annotation Types'

    def __str__(self):
        return u'{}'.format(self.input_type)


class Layers(models.Model):
    id = models.BigAutoField(primary_key=True)
    prep = models.ForeignKey(Animal, models.CASCADE, null=True, db_column="prep_id", verbose_name="Animal")
    
    structure = models.ForeignKey(Structure, models.CASCADE, null=True, db_column="structure_id",
                               verbose_name="Structure")
    person = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column="person_id",
                               verbose_name="Creator", blank=False, null=False, related_name="creator")
    updatedby = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column="updated_by",
                               verbose_name="Updater", blank=True, null=True, related_name="updater")
    input_type = models.ForeignKey(InputType, models.CASCADE, db_column="input_type_id",
                               verbose_name="Input", blank=False, null=False)
    layer = models.CharField(max_length=255)
    x = models.FloatField(verbose_name="X (um)")
    y = models.FloatField(verbose_name="Y (um)")
    section = models.FloatField(verbose_name="Section (um)")
    active = models.BooleanField(default=True, db_column='active')
    created = models.DateTimeField(auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        abstract = True


class LayerData(Layers):

    class Meta:
        managed = True
        db_table = 'layer_data'
        verbose_name = 'Annotation Data'
        verbose_name_plural = 'Annotation Data'

    def __str__(self):
        return u'{} {}'.format(self.prep, self.layer)

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