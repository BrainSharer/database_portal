from datetime import datetime
from neuroglancer.atlas import update_center_of_mass
from rest_framework import serializers
from rest_framework.exceptions import APIException
import logging

from brain.models import Animal
from neuroglancer.models import LayerData, Structure, UrlModel
from django.contrib.auth.models import User

logging.basicConfig()
logger = logging.getLogger(__name__)


class AnimalInputSerializer(serializers.Serializer):
    animal = serializers.CharField()


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class AnnotationSerializer(serializers.Serializer):
    """
    This one feeds the data import
    """
    id = serializers.CharField()
    point = serializers.ListField()
    type = serializers.CharField()
    description = serializers.CharField()


class LineSerializer(serializers.Serializer):
    """
    This one feeds the data import
    """
    id = serializers.CharField()
    pointA = serializers.ListField()
    pointB = serializers.ListField()
    type = serializers.CharField()
    description = serializers.CharField()


class AnnotationsSerializer(serializers.Serializer):
    """
    This one feeds the dropdown
    """
    prep_id = serializers.CharField()
    layer = serializers.CharField()
    input_type = serializers.CharField()
    input_type_id = serializers.IntegerField()


class StructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Structure
        fields = '__all__'


class LayerDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayerData
        fields = '__all__'


class CenterOfMassSerializer(serializers.ModelSerializer):
    """Takes care of entering a set of points"""
    structure_id = serializers.CharField()

    class Meta:
        model = LayerData
        fields = '__all__'

    def create(self, validated_data):
        logger.debug('Creating COM')
        com = LayerData(
            x=validated_data['x'],
            y=validated_data['y'],
            section=validated_data['section'],
            active=True,
            created=datetime.now()
        )
        try:
            structure = Structure.objects.get(
                abbreviation__exact=validated_data['structure_id'])
            com.structure = structure
        except APIException as e:
            logger.error(f'Error with structure {e}')

        try:
            prep = Animal.objects.get(prep_id=validated_data['prep'])
            com.prep = prep
        except Animal.DoesNotExist:
            logger.error('Error with animal')
        try:
            com.save()
        except APIException as e:
            logger.error(f'Could not save center of mass: {e}')

        return com


class RotationModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="person__username")

    class Meta:
        model = LayerData
        fields = ['prep_id', 'input_type_id', 'person_id', 'username']


class RotationSerializer(serializers.Serializer):
    prep_id = serializers.CharField()
    input_type = serializers.CharField()
    person_id = serializers.IntegerField()
    username = serializers.CharField()


class UrlSerializer(serializers.ModelSerializer):
    """Override method of entering a url into the DB.
    The url can't be in the UrlModel when it is returned
    to neuroglancer as it crashes neuroglancer."""
    person_id = serializers.IntegerField()

    class Meta:
        model = UrlModel
        fields = '__all__'
        ordering = ['-created']

    def create(self, validated_data):
        """
        This gets called when a user clicks New in Neuroglancer
        """
        urlModel = UrlModel(
            url=validated_data['url'],
            user_date=validated_data['user_date'],
            comments=validated_data['comments'],
            public=False,
            vetted=False,
        )
        if 'person_id' in validated_data:
            try:
                authUser = User.objects.get(pk=validated_data['person_id'])
                urlModel.person = authUser
            except User.DoesNotExist:
                logger.error('Person was not in validated data')
        try:
            urlModel.save()
        except APIException:
            logger.error('Could not save url model')
        update_center_of_mass(urlModel)
        urlModel.url = None
        return urlModel

    def update(self, instance, validated_data):
        """
        This gets called when a user clicks Save in Neuroglancer
        """
        instance.url = validated_data.get('url', instance.url)
        instance.user_date = validated_data.get(
            'user_date', instance.user_date)
        instance.comments = validated_data.get('comments', instance.comments)
        if 'person_id' in validated_data:
            try:
                authUser = User.objects.get(pk=validated_data['person_id'])
                instance.person = authUser
            except User.DoesNotExist:
                logger.error('Person was not in validated data')
        try:
            instance.save()
        except APIException:
            logger.error('Could not save url model')
        update_center_of_mass(instance)
        instance.url = None
        return instance
