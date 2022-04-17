# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import EnumField
from django.utils.safestring import mark_safe
from authentication.models import Lab
from django.core.validators import MaxValueValidator, MinValueValidator
import os


class AtlasModel(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Biocyc(AtlasModel):
    bio_name = models.CharField(max_length=20, verbose_name="Biosource (species)", blank=False, null=False)    
    class Meta:
        managed = True
        db_table = 'biocyc'
        verbose_name = 'Biocyc (species)'
        verbose_name_plural = 'Biocyc (species)'
        
    def __str__(self):
        return u'{}'.format(self.bio_name)

class Animal(AtlasModel):
    animal_name = models.CharField(max_length=20, verbose_name="Animal name")
    lab = models.ForeignKey(Lab, models.CASCADE, blank=False, null=False)
    biocyc = models.ForeignKey(Biocyc, models.CASCADE, blank=False, null=False, db_column='FK_ORGID')
    comments = models.TextField(max_length=2001, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'biosource'
        verbose_name = 'Biosource (animal)'
        verbose_name_plural = 'Biosource (animals)'

    def __str__(self):
        return u'{}'.format(self.animal_name)


class Injection(AtlasModel):
    animal = models.ForeignKey(Animal, models.CASCADE, db_column='FK_biosource_id')
    performance_center = models.ForeignKey(Lab, models.DO_NOTHING, blank=True, null=True, db_column='FK_performance_center_id')
    anesthesia = EnumField(choices=['ketamine','isoflurane'], blank=True, null=True)
    method = EnumField(choices=['iontophoresis','pressure','volume'], blank=True, null=True)
    pipet = EnumField(choices=['glass','quartz','Hamilton','syringe needle'], blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    angle = models.CharField(max_length=20, blank=True, null=True)
    brain_location_dv = models.FloatField()
    brain_location_ml = models.FloatField()
    brain_location_ap = models.FloatField()
    injection_date = models.DateField(blank=True, null=True)
    transport_days = models.IntegerField()
    virus_count = models.IntegerField()
    comments = models.TextField(max_length=2001, blank=True, null=True)    
    injection_volume_ul = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'injection'
        verbose_name = 'Injection'
        verbose_name_plural = 'Injections'

    def __str__(self):
        return "{} {}".format(self.animal.animal, self.comments)


class Virus(AtlasModel):
    virus_name = models.CharField(max_length=50)
    virus_type = EnumField(choices=['Adenovirus','AAV','CAV','DG rabies','G-pseudo-Lenti','Herpes','Lenti','N2C rabies','Sinbis'], blank=True, null=True)
    virus_active = EnumField(choices=['yes','no'], blank=True, null=True)
    type_details = models.CharField(max_length=500, blank=True, null=True)
    titer = models.FloatField()
    lot_number = models.CharField(max_length=20, blank=True, null=True)
    label = EnumField(choices=['YFP','GFP','RFP','histo-tag'], blank=True, null=True)
    label2 = models.CharField(max_length=200, blank=True, null=True)
    excitation_1p_wavelength = models.IntegerField()
    excitation_1p_range = models.IntegerField()
    excitation_2p_wavelength = models.IntegerField()
    excitation_2p_range = models.IntegerField()
    lp_dichroic_cut = models.IntegerField()
    emission_wavelength = models.IntegerField()
    emission_range = models.IntegerField()
    virus_source = EnumField(choices=['Adgene','Salk','Penn','UNC'], blank=True, null=True)
    source_details = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'virus'
        verbose_name = 'Virus'
        verbose_name_plural = 'Viruses'

    def __str__(self):
        return self.virus_name

class InjectionVirus(AtlasModel):
    injection = models.ForeignKey(Injection, models.CASCADE, db_column='FK_injection_id')
    virus = models.ForeignKey('Virus', models.CASCADE, db_column='FK_virus_id')

    class Meta:
        managed = True
        db_table = 'injection_virus'
        verbose_name = 'Injection Virus'
        verbose_name_plural = 'Injection Viruses'


class ScanRun(AtlasModel):
    animal = models.ForeignKey(Animal, models.CASCADE, db_column='FK_biosource_id')
    objective = EnumField(choices=['60X','40X','20X','10X'], blank=True, null=True)
    resolution = models.FloatField(verbose_name="XY Resolution (um)")
    zresolution = models.FloatField(verbose_name="Z Resolution (um)")
    number_of_slides = models.IntegerField()
    scan_date = models.DateField(blank=True, null=True)
    file_type = EnumField(choices=['CZI','JPEG2000','NDPI','NGR'], blank=True, null=True)
    channels_per_scene = EnumField(choices=['1','2','3','4'], blank=True, null=True)

    width = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(80000)], 
                                default=0, verbose_name="Width (pixels)")
    height = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(75000)], 
                                 default=0, verbose_name="Height (pixels)")
    comments = models.TextField(max_length=2001, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'scan_run'

    def __str__(self):
        return "{} Scan ID: {}".format(self.animal, self.id)

class BrainAtlas(AtlasModel):
    atlas_name = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(max_length=2001, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'brain_atlas'
        verbose_name = 'Brain atlas'
        verbose_name_plural = 'Brain atlases'

    def __str__(self):
        return self.atlas_name


class BrainRegion(AtlasModel):
    abbreviation = models.CharField(max_length=200)
    description = models.TextField(max_length=2001, blank=True, null=True)
    brain_atlas = models.ForeignKey(BrainAtlas, models.CASCADE, db_column='FK_ref_atlas_id')
    
    class Meta:
        managed = True
        db_table = 'brain_region'
        verbose_name = 'Brain region'
        verbose_name_plural = 'Brain regions'

    def __str__(self):
        return f'{self.description} {self.abbreviation}'
