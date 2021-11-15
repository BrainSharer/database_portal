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
from django.core.validators import MaxValueValidator, MinValueValidator
import os


class AtlasModel(models.Model):
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Animal(AtlasModel):
    prep_id = models.CharField(primary_key=True, max_length=20)
    performance_center = EnumField(choices=['CSHL','Salk','UCSD','HHMI','Duke'], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    species = EnumField(choices=['mouse','rat'], blank=True, null=True)
    strain = models.CharField(max_length=15, blank=True, null=True)
    sex = EnumField(choices=['M','F'], blank=True, null=True)
    genotype = models.CharField(max_length=100, blank=True, null=True)
    breeder_line = models.CharField(max_length=100, blank=True, null=True)
    vender = EnumField(choices=['Jackson','Charles River','Harlan','NIH','Taconic'], blank=True, null=True)
    stock_number = models.CharField(max_length=100, blank=True, null=True)
    tissue_source = EnumField(choices=['animal','brain','slides'], blank=True, null=True)
    ship_date = models.DateField(blank=True, null=True)
    shipper = EnumField(choices=['FedEx','UPS'], blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    # cshl_send_date = models.DateField(blank=True, null=True, verbose_name='CSHL ship date')
    aliases_1 = models.CharField(max_length=100, blank=True, null=True)
    aliases_2 = models.CharField(max_length=100, blank=True, null=True)
    aliases_3 = models.CharField(max_length=100, blank=True, null=True)
    aliases_4 = models.CharField(max_length=100, blank=True, null=True)
    aliases_5 = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(max_length=2001, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'animal'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'

    def __str__(self):
        return u'{}'.format(self.prep_id)

    def histogram(self):
        links = []
        png = f'{self.prep_id}.png'
        for channel in [1,2,3]:
            testfile = f'/net/birdstore/Active_Atlas_Data/data_root/pipeline_data/{self.prep_id}/histogram/CH{channel}/{png}'
            if os.path.isfile(testfile):
                histogram = f'/data/{self.prep_id}/histogram/CH{channel}/{png}'
                link = f'<div class="hover_img"><a href="#">CH{channel}<span><img src="https://activebrainatlas.ucsd.edu/{histogram}" /></span></a></div>' 
                links.append(link)

        return mark_safe(' '.join(links))

    histogram.short_description = 'Histogram'

class FileOperation(AtlasModel):
    id = models.AutoField(primary_key=True)
    tif = models.ForeignKey('SlideCziToTif', models.CASCADE)
    operation = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    file_size = models.FloatField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'file_operation'
        verbose_name = 'File Operation'
        verbose_name_plural = 'File Operations'

class Histology(AtlasModel):
    id = models.AutoField(primary_key=True)
    prep = models.ForeignKey(Animal, models.CASCADE)
    virus = models.ForeignKey('Virus', models.CASCADE, blank=True, null=True)
    label = models.ForeignKey('OrganicLabel', models.CASCADE, blank=True, null=True)
    performance_center = EnumField(choices=['CSHL','Salk','UCSD','HHMI'], blank=True, null=True)
    anesthesia = EnumField(choices=['ketamine','isoflurane','pentobarbital','fatal plus'], blank=True, null=True)
    perfusion_age_in_days = models.PositiveIntegerField()
    perfusion_date = models.DateField(blank=True, null=True)
    exsangination_method = EnumField(choices=['PBS','aCSF','Ringers'], blank=True, null=True)
    fixative_method = EnumField(choices=['Para','Glut','Post fix'], blank=True, null=True)
    special_perfusion_notes = models.CharField(max_length=200, blank=True, null=True)
    post_fixation_period = models.PositiveIntegerField()
    whole_brain = models.CharField(max_length=1, blank=True, null=True)
    block = models.CharField(max_length=200, blank=True, null=True)
    date_sectioned = models.DateField(blank=True, null=True)
    side_sectioned_first = EnumField(choices=[('ASC', 'Left'), ('DESC','Right')], blank=False, null=False, default = 'ASC')
    sectioning_method = EnumField(choices=['cryoJane','cryostat','vibratome','optical','sliding microtiome'], blank=True, null=True)
    section_thickness = models.PositiveIntegerField()
    orientation = EnumField(choices=['coronal','horizontal','sagittal','oblique'], blank=True, null=True)
    oblique_notes = models.CharField(max_length=200, blank=True, null=True)
    mounting = EnumField(choices=['every section','2nd','3rd','4th','5ft','6th'], blank=True, null=True)
    counterstain = EnumField(choices=['thionin','NtB','NtFR','DAPI','Giemsa','Syto41'], blank=True, null=True)
    comments = models.TextField(max_length=2001, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'histology'
        verbose_name = 'Histology'
        verbose_name_plural = 'Histologies'

    def __str__(self):
        if self.virus is not None and self.virus.virus_name is not None:
            histology_label = u'{} {}'.format(self.prep.prep_id, self.virus.virus_name)
        else:
            histology_label = u'{}'.format(self.prep.prep_id)

        return histology_label

class Injection(AtlasModel):
    id = models.AutoField(primary_key=True)
    prep = models.ForeignKey(Animal, models.CASCADE)
    label = models.ForeignKey('OrganicLabel', models.CASCADE, blank=True, null=True)
    performance_center = EnumField(choices=['CSHL','Salk','UCSD','HHMI','Duke'], blank=True, null=True)
    anesthesia = EnumField(choices=['ketamine','isoflurane'], blank=True, null=True)
    method = EnumField(choices=['iontophoresis','pressure','volume'], blank=True, null=True)
    injection_volume = models.FloatField()
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

    class Meta:
        managed = False
        db_table = 'injection'
        verbose_name = 'Injection'
        verbose_name_plural = 'Injections'

    def __str__(self):
        return "{} {}".format(self.prep.prep_id, self.comments)

class InjectionVirus(AtlasModel):
    id = models.AutoField(primary_key=True)
    injection = models.ForeignKey(Injection, models.CASCADE)
    virus = models.ForeignKey('Virus', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'injection_virus'
        verbose_name = 'Injection Virus'
        verbose_name_plural = 'Injection Viruses'

class OrganicLabel(AtlasModel):
    id = models.AutoField(primary_key=True)
    label_id = models.CharField(max_length=20)
    label_type = EnumField(choices=['Cascade Blue','Chicago Blue','Alexa405','Alexa488','Alexa647','Cy2','Cy3','Cy5','Cy5.5','Cy7','Fluorescein','Rhodamine B','Rhodamine 6G','Texas Red','TMR'], blank=True, null=True)
    type_lot_number = models.CharField(max_length=20, blank=True, null=True)
    type_tracer = EnumField(choices=['BDA','Dextran','FluoroGold','DiI','DiO'], blank=True, null=True)
    type_details = models.CharField(max_length=500, blank=True, null=True)
    concentration = models.FloatField()
    excitation_1p_wavelength = models.IntegerField()
    excitation_1p_range = models.IntegerField()
    excitation_2p_wavelength = models.IntegerField()
    excitation_2p_range = models.IntegerField()
    lp_dichroic_cut = models.IntegerField()
    emission_wavelength = models.IntegerField()
    emission_range = models.IntegerField()
    label_source = EnumField(choices=['Invitrogen','Sigma','Thermo-Fisher'], blank=True, null=True)
    source_details = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organic_label'
        verbose_name = 'Organic Label'
        verbose_name_plural = 'Organic Labels'

    def __str__(self):
        return "{} {}".format(self.label_id, self.label_type)

class ScanRun(AtlasModel):
    id = models.AutoField(primary_key=True)
    prep = models.ForeignKey(Animal, models.CASCADE)
    performance_center = EnumField(choices=['CSHL','Salk','UCSD','HHMI'], blank=True, null=True)
    machine = EnumField(choices=['Invitrogen','Sigma','Thermo-Fisher'], blank=True, null=True)
    objective = EnumField(choices=['60X','40X','20X','10X'], blank=True, null=True)
    resolution = models.FloatField(verbose_name="XY Resolution (um)")
    zresolution = models.FloatField(verbose_name="Z Resolution (um)")
    number_of_slides = models.IntegerField()
    scan_date = models.DateField(blank=True, null=True)
    file_type = EnumField(choices=['CZI','JPEG2000','NDPI','NGR'], blank=True, null=True)
    channels_per_scene = EnumField(choices=['1','2','3','4'], blank=True, null=True)
    converted_status = EnumField(choices=['not started','converted','converting','error'], blank=True, null=True)
    ch_1_filter_set = EnumField(choices=['68','47','38','46','63','64','50'], blank=True, null=True)
    ch_2_filter_set = EnumField(choices=['68','47','38','46','63','64','50'], blank=True, null=True)
    ch_3_filter_set = EnumField(choices=['68','47','38','46','63','64','50'], blank=True, null=True)
    ch_4_filter_set = EnumField(choices=['68','47','38','46','63','64','50'], blank=True, null=True)

    width = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(80000)], 
                                default=0, verbose_name="Width (pixels)")
    height = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(75000)], 
                                 default=0, verbose_name="Height (pixels)")
    rotation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    flip = EnumField(choices=['none','flip','flop'], blank=False, null=False, default='none')

    comments = models.TextField(max_length=2001, blank=True, null=True)

    def __str__(self):
        return "{} Scan ID: {}".format(self.prep.prep_id, self.id)

    class Meta:
        managed = False
        db_table = 'scan_run'

class Slide(AtlasModel):
    id = models.AutoField(primary_key=True)
    scan_run = models.ForeignKey(ScanRun, models.CASCADE)
    slide_physical_id = models.IntegerField()
    rescan_number = EnumField(choices=['1','2','3'], blank=False, null=False, default='1')
    slide_status = EnumField(choices=['Bad','Good'], blank=False, null=False)
    scenes = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(6)])
    insert_before_one = models.IntegerField(blank=False, null=False, default=0,
                                            verbose_name='Replicate S1',
                                            validators=[MinValueValidator(0),MaxValueValidator(5)])
    OUTOFFOCUS = 1
    BADTISSUE = 2
    END = 3
    OK = 0
    QC_CHOICES = (
        (OUTOFFOCUS, 'Out-of-Focus'),
        (BADTISSUE, 'Bad tissue'),
        (END, 'End'),
        (OK, 'OK'),
    )
    scene_qc_1 = models.IntegerField(choices=QC_CHOICES, default=0, verbose_name='Scene 1 QC')
    insert_between_one_two = models.IntegerField(blank=False, null=False, default=0,
                                                 verbose_name='Replicate S2',
                                                 validators=[MinValueValidator(0),MaxValueValidator(5)])
    scene_qc_2 = models.IntegerField(choices=QC_CHOICES, default=0, verbose_name='Scene 2 QC')
    insert_between_two_three = models.IntegerField(blank=False, null=False, default=0,
                                                   verbose_name='Replicate S3',
                                                   validators=[MinValueValidator(0),MaxValueValidator(5)])
    scene_qc_3 = models.IntegerField(choices=QC_CHOICES, default=0, verbose_name='Scene 3 QC')
    insert_between_three_four = models.IntegerField(blank=False, null=False, default=0,
                                                    verbose_name='Replicate S4',
                                                    validators=[MinValueValidator(0),MaxValueValidator(5)])
    scene_qc_4 = models.IntegerField(choices=QC_CHOICES, default=0, verbose_name='Scene 4 QC')
    insert_between_four_five = models.IntegerField(blank=False, null=False, default=0,
                                                   verbose_name='Replicate S5',
                                                   validators=[MinValueValidator(0),MaxValueValidator(5)])
    scene_qc_5 = models.IntegerField(choices=QC_CHOICES, default=0, verbose_name='Scene 5 QC')
    insert_between_five_six = models.IntegerField(blank=False, null=False, default=0,
                                                  verbose_name='Replicate S6',
                                                  validators=[MinValueValidator(0),MaxValueValidator(5)])
    scene_qc_6 = models.IntegerField(choices=QC_CHOICES, default=0, verbose_name='Scene 6 QC')
    file_name = models.CharField(max_length=200)
    comments = models.TextField(max_length=2001, blank=True, null=True)
    file_size = models.FloatField(verbose_name='File size (bytes)')
    processed = models.BooleanField(verbose_name="Converted")


    def __str__(self):
        return "{}".format(self.file_name)

    class Meta:
        managed = False
        db_table = 'slide'

class SlideCziToTif(AtlasModel):
    id = models.AutoField(primary_key=True)
    slide = models.ForeignKey(Slide, models.CASCADE, related_name='slideczis')
    file_name = models.CharField(max_length=200, null=False)
    scene_number = models.IntegerField(blank=False, null=False, default=1,
                                                    verbose_name='Scene',
                                                    validators=[MinValueValidator(1),MaxValueValidator(6)])
    scene_index = models.IntegerField()
    channel = models.IntegerField()
    width = models.IntegerField(verbose_name='Width (pixels)')
    height = models.IntegerField(verbose_name='Height (pixels)')
    comments = models.TextField(max_length=2000, blank=True, null=True)
    file_size = models.FloatField(verbose_name='File size (bytes)')
    processing_duration = models.FloatField(verbose_name="Processing time (seconds)")



    def max_scene(self):
        return self.slide.scenes

    class Meta():
        managed = False
        db_table = 'slide_czi_to_tif'
        verbose_name = 'Slide CZI to TIF'
        verbose_name_plural = 'Slides CZI to TIF'
        ordering = ['scene_number', 'channel']

    def __str__(self):
        return "{}".format(self.file_name)

class Section(AtlasModel):
    id = models.AutoField(primary_key=True)
    prep_id = models.CharField(max_length=20)
    czi_file = models.CharField(max_length=200)
    slide_physical_id = models.IntegerField(null=False, verbose_name='Slide')
    file_name = models.CharField(max_length=200)
    tif = models.ForeignKey(SlideCziToTif, models.DO_NOTHING, db_column='tif_id')
    scene_number = models.IntegerField(null=False, verbose_name='Scene')
    scene_index = models.IntegerField(null=False, verbose_name='Scene Index')
    channel = models.IntegerField(null=False)

    def tif(self):
        return self.file_name

    def slide(self):
        return self.slide_physical_id

    def scene(self):
        return self.scene_number

    class Meta:
        managed = False
        db_table = 'sections'
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return self.file_name

    def histogram(self):
        png = self.file_name.replace('tif','png')
        testfile = "/net/birdstore/Active_Atlas_Data/data_root/pipeline_data/{}/histogram/CH1/{}".format(self.prep_id, png)
        if os.path.isfile(testfile):
            histogram = "https://activebrainatlas.ucsd.edu/data/{}/histogram/CH1/{}".format(self.prep_id, png)
            return mark_safe(
            '<div class="profile-pic-wrapper"><img src="{}" /></div>'.format(histogram) )
        else:
            return mark_safe('<div>Not available</div>')
    histogram.short_description = 'Histogram'

    def image_tag(self):
        png = self.file_name.replace('tif', 'png')
        # http://localhost:8000/data/DK39/thumbnail/DK39_ID_0002_slide058_S1_C2.png
        testfile = "/net/birdstore/Active_Atlas_Data/data_root/pipeline_data/{}/www/{}".format(self.prep_id, png)
        if os.path.isfile(testfile):
            thumbnail = "https://activebrainatlas.ucsd.edu/data/{}/www/{}".format(self.prep_id, png)
            return mark_safe(
                '<div class="profile-pic-wrapper"><img src="{}" /></div>'.format(thumbnail))
        else:
            return mark_safe('<div>Not available</div>')

    image_tag.short_description = 'Image'

class Virus(AtlasModel):
    id = models.AutoField(primary_key=True)
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
        managed = False
        db_table = 'virus'
        verbose_name = 'Virus'
        verbose_name_plural = 'Viruses'

    def __str__(self):
        return self.virus_name
