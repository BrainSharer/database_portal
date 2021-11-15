from django.db import models
from django.conf import settings
from django.utils.html import escape
import re
import json
import pandas as pd
from enum import Enum
from django.template.defaultfilters import truncatechars
from brain.models import AtlasModel, Animal
from django_mysql.models import EnumField

COL_LENGTH = 1000
ROW_LENGTH = 1000
Z_LENGTH = 300
ATLAS_X_BOX_SCALE = 10
ATLAS_Y_BOX_SCALE = 10
ATLAS_Z_BOX_SCALE = 20
ATLAS_RAW_SCALE = 10
ANNOTATION_ID = 52
LAUREN_ID = 16

class AnnotationChoice(str, Enum):
    POINT = 'point'
    LINE = 'line'

    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    def __str__(self):
        return self.value

class UrlModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.JSONField()
    person = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, db_column="person_id",
                               verbose_name="User")
    public = models.BooleanField(default = True, db_column='active')
    vetted = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    user_date = models.CharField(max_length=25)
    comments = models.CharField(max_length=255)

    @property
    def short_description(self):
        return truncatechars(self.url, 50)

    @property
    def escape_url(self):
        return escape(self.url)

    @property
    def animal(self):
        """
        find the animal within the url between data/ and /neuroglancer_data:
        data/MD589/neuroglancer_data/C1
        return: the first match if found, otherwise NA
        """
        animal = "NA"
        match = re.search('data/(.+?)/neuroglancer_data', str(self.url))
        if match is not None and match.group(1) is not None:
            animal = match.group(1)
        return animal

    @property
    def point_frame(self):
        df = None
        if self.url is not None:
            point_data = self.find_values('annotations', self.url)
            if len(point_data) > 0:
                d = [row['point'] for row in point_data[0]]
                df = pd.DataFrame(d, columns=['X', 'Y', 'Section'])
                df = df.round(decimals=0)
        return df

    @property
    def points(self):
        result = None
        dfs = []
        if self.url is not None:
            json_txt = self.url
            layers = json_txt['layers']
            for layer in layers:
                if 'annotations' in layer:
                    name = layer['name']
                    annotation = layer['annotations']
                    d = [row['point'] for row in annotation if 'point' in row and 'pointA' not in row]
                    df = pd.DataFrame(d, columns=['X', 'Y', 'Section'])
                    df['Section'] = df['Section'].astype(int)
                    df['Layer'] = name
                    structures = [row['description'] for row in annotation if 'description' in row]
                    if len(structures) != len(df):
                        structures = ['' for row in annotation if 'point' in row and 'pointA' not in row]
                    df['Description'] = structures
                    df = df[['Layer', 'Description', 'X', 'Y', 'Section']]
                    dfs.append(df)
            if len(dfs) == 0:
                result = None
            elif len(dfs) == 1:
                result = dfs[0]
            else:
                result = pd.concat(dfs)

        return result

    @property
    def layers(self):
        layer_list = []
        if self.url is not None:
            json_txt = self.url
            layers = json_txt['layers']
            for layer in layers:
                if 'annotations' in layer:
                    layer_name = layer['name']
                    layer_list.append(layer_name)

        return layer_list

    class Meta:
        managed = False
        verbose_name = "Url"
        verbose_name_plural = "Urls"
        ordering = ('comments', 'created')
        db_table = 'neuroglancer_urls'

    def __str__(self):
        return u'{}'.format(self.comments)

    @property
    def point_count(self):
        result = "display:none;"
        if self.points is not None:
            df = self.points
            df = df[(df.Layer == 'PM nucleus') | (df.Layer == 'premotor')]
            if len(df) > 0:
                result = "display:inline;"
        return result


    def find_values(self, id, json_repr):
        results = []

        def _decode_dict(a_dict):
            try:
                results.append(a_dict[id])
            except KeyError:
                pass
            return a_dict

        json.loads(json_repr, object_hook=_decode_dict)  # Return value ignored.
        return results

class Points(UrlModel):

    class Meta:
        managed = False
        proxy = True
        verbose_name = 'Points'
        verbose_name_plural = 'Points'

class Structure(AtlasModel):
    id = models.BigAutoField(primary_key=True)
    abbreviation = models.CharField(max_length=200)
    description = models.TextField(max_length=2001, blank=False, null=False)
    color = models.PositiveIntegerField()
    hexadecimal = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'structure'
        verbose_name = 'Structure'
        verbose_name_plural = 'Structures'

    def __str__(self):
        return f'{self.description} {self.abbreviation}'

class InputType(models.Model):
    id = models.BigAutoField(primary_key=True)
    input_type = models.CharField(max_length=50, blank=False, null=False, verbose_name='Input')
    description = models.TextField(max_length=255, blank=False, null=False)
    active = models.BooleanField(default = True, db_column='active')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'com_type'
        verbose_name = 'COM Type'
        verbose_name_plural = 'COM Types'

    def __str__(self):
        return u'{}'.format(self.input_type)

class Transformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    prep = models.ForeignKey(Animal, models.CASCADE, null=True, db_column="prep_id", verbose_name="Animal")
    person = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column="person_id",
                               verbose_name="User", blank=False, null=False)
    input_type = models.ForeignKey(InputType, models.CASCADE, db_column="input_type_id",
                               verbose_name="Input", blank=False, null=False)
    com_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")
    active = models.BooleanField(default = True, db_column='active')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'transformation'
        verbose_name = 'Transformation'
        verbose_name_plural = 'Transformations'

    def __str__(self):
        return u'{} {}'.format(self.prep.prep_id, self.com_name)

class Layers(models.Model):
    id = models.BigAutoField(primary_key=True)
    # url = models.ForeignKey(UrlModel, models.CASCADE, null=True, db_column="url_id",
    #                            verbose_name="Url")
    prep = models.ForeignKey(Animal, models.CASCADE, null=True, db_column="prep_id", verbose_name="Animal")
    
    structure = models.ForeignKey(Structure, models.CASCADE, null=True, db_column="structure_id",
                               verbose_name="Structure")
    person = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column="person_id",
                               verbose_name="Creator", blank=False, null=False, related_name="creator")
    updatedby = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, db_column="updated_by",
                               verbose_name="Updater", blank=True, null=True, related_name="updater")
    input_type = models.ForeignKey(InputType, models.CASCADE, db_column="input_type_id",
                               verbose_name="Input", blank=False, null=False)
    vetted = EnumField(choices=['yes','no'], blank=True, null=True)
    layer = models.CharField(max_length=255)
    x = models.FloatField(verbose_name="X (um)")
    y = models.FloatField(verbose_name="Y (um)")
    section = models.FloatField(verbose_name="Section (um)")
    # segment_id = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default = True, db_column='active')
    created = models.DateTimeField(auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        abstract = True

class LayerData(Layers):

    class Meta:
        managed = False
        db_table = 'layer_data'
        verbose_name = 'Annotation Data'
        verbose_name_plural = 'Annotation Data'

    def __str__(self):
        return u'{} {}'.format(self.prep, self.layer)


class AlignmentScore(models.Model):
    class Meta:
        managed = False
        db_table = 'layer_data'
        verbose_name = 'Alignment Score'
        verbose_name_plural = 'Alignment Scores'

    def __str__(self):
        return u'{}'.format(self.prep_id)