from django.db import models
from django.conf import settings
from django.utils.html import escape
import re
from enum import Enum
from django.template.defaultfilters import truncatechars
from brain.models import Animal, BrainRegion


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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, db_column="owner_id",
                               verbose_name="User")
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


class AnnotationAbstract(models.Model):
    id = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, models.CASCADE, null=True, db_column="FK_animal_id", verbose_name="Animal")
    brain_region = models.ForeignKey(BrainRegion, models.CASCADE, null=True, db_column="FK_structure_id",
                               verbose_name="Structure")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column="FK_owner_id",
                               verbose_name="Owner", blank=False, null=False)
    input_type = models.ForeignKey(InputType, models.CASCADE, db_column="input_type_id",
                               verbose_name="Input", blank=False, null=False)
    layer = models.CharField(max_length=255)
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
        return u'{} {}'.format(self.animal, self.layer)


class AnnotationPointArchive(AnnotationAbstract):
    archive = models.ForeignKey(ArchiveSet, models.CASCADE, 
                               verbose_name="Archive Set", blank=True, null=True, 
                               db_column='FK_archive_set_id')

    class Meta:
        managed = True
        db_table = 'annotations_point_archive'
        verbose_name = 'Annotation Point Archive'
        verbose_name_plural = 'Annotation Points Archive'


