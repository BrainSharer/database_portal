from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import APIException
import logging

from brain.models import Animal
from neuroglancer.models import LayerData, Structure, NeuroglancerModel
from neuroglancer.atlas import update_annotation_data
from authentication.models import User

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



class NeuroglancerSerializer(serializers.ModelSerializer):
    """Override method of entering a neuroglancer_state into the DB.
    The neuroglancer_state can't be in the NeuroglancerModel when it is returned
    to neuroglancer as it crashes neuroglancer."""
    person_id = serializers.IntegerField()

    class Meta:
        model = NeuroglancerModel
        fields = '__all__'
        ordering = ['-created']

    def create(self, validated_data):
        """
        This gets called when a user clicks New in Neuroglancer
        """
        neuroglancerModel = NeuroglancerModel(
            neuroglancer_state=validated_data['neuroglancer_state'],
            user_date=validated_data['user_date'],
            comments=validated_data['comments'],
            vetted=False,
        )
        if 'person_id' in validated_data:
            try:
                authUser = User.objects.get(pk=validated_data['person_id'])
                neuroglancerModel.person = authUser
                # neuroglancerModel.lab = authUser.lab
            except User.DoesNotExist:
                logger.error('Person was not in validated data')
                return
        try:
            neuroglancerModel.save()
        except APIException:
            logger.error('Could not save neuroglancer model')
        update_annotation_data(neuroglancerModel)
        neuroglancerModel.neuroglancer_state = None
        return neuroglancerModel

    def update(self, instance, validated_data):
        """
        This gets called when a user clicks Save in Neuroglancer
        """
        instance.neuroglancer_state = validated_data.get('neuroglancer_state', instance.neuroglancer_state)
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
            logger.error('Could not save Neuroglancer model')
        update_annotation_data(instance)
        instance.neuroglancer_state = None
        return instance

class NeuronSerializer(serializers.Serializer):
    """
    This one feeds the data import
    """
    idstring = serializers.ListField()