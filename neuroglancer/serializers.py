from rest_framework import serializers
from rest_framework import serializers
from rest_framework.exceptions import APIException
import logging

from brain.models import BrainRegion
from neuroglancer.models import AnnotationPoints, NeuroglancerModel, NeuroglancerView
from neuroglancer.atlas import update_annotation_data

logging.basicConfig()
logger = logging.getLogger('django')

class AnimalInputSerializer(serializers.Serializer):
    animal = serializers.CharField()


class AnnotationSerializer(serializers.Serializer):
    """
    This one feeds the data import
    Note, this is the singular one!
    """
    id = serializers.CharField()
    point = serializers.ListField()
    type = serializers.CharField()
    description = serializers.CharField()


class AnnotationsSerializer(serializers.Serializer):
    """
    This one feeds the dropdown
    Note, this is the plural one!
    """
    animal_id = serializers.IntegerField()
    animal_name = serializers.CharField()
    label = serializers.CharField()

class AnnotationPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationPoints
        fields = '__all__'


class BrainRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrainRegion
        fields = '__all__'


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class LineSerializer(serializers.Serializer):
    """
    This one feeds the data import
    """
    id = serializers.CharField()
    pointA = serializers.ListField()
    pointB = serializers.ListField()
    type = serializers.CharField()
    description = serializers.CharField()


class NeuroglancerSerializer(serializers.ModelSerializer):
    """Override method of entering a neuroglancer_state into the DB.
    The neuroglancer_state can't be in the NeuroglancerModel when it is returned
    to neuroglancer as it crashes neuroglancer."""
    lab = serializers.CharField()

    class Meta:
        model = NeuroglancerModel
        fields = '__all__'
        ordering = ['-created']
        

    def create(self, validated_data):
        """
        This gets called when a user clicks New in Neuroglancer
        """
        obj = NeuroglancerModel(
            neuroglancer_state=validated_data['neuroglancer_state'],
            user_date=validated_data['user_date'],
            comments=validated_data['comments'],
        )
        if 'owner' in validated_data:
            owner = validated_data['owner']
            obj = self.take_care_of_owner(obj, owner)
        return obj

    def update(self, obj, validated_data):
        """
        This gets called when a user clicks Save in Neuroglancer
        """
        obj.neuroglancer_state = validated_data.get('neuroglancer_state', obj.neuroglancer_state)
        obj.user_date = validated_data.get('user_date', obj.user_date)
        obj.comments = validated_data.get('comments', obj.comments)
        if 'owner' in validated_data:
            owner = validated_data['owner']
            obj = self.take_care_of_owner(obj, owner)
        return obj

    def take_care_of_owner(self, obj, owner):
        '''
        Takes care of tasks that are in both create and update
        :param obj: the neuroglancerModel object
        :param owner: the owner from the validated_data
        '''
        obj.owner = owner
        obj.owner.lab = owner.lab
        try:
            obj.save()
        except APIException:
            logger.error('Could not save Neuroglancer model')
        update_annotation_data(obj)
        obj.neuroglancer_state = None
        return obj

class NeuroglancerGroupViewSerializer(serializers.ModelSerializer):
    '''
    This is to form the groups with just distinct group_name
    and layer_type
    '''

    class Meta:
        model = NeuroglancerView
        fields = ['group_name', 'layer_type']
        ordering = ['group_name', 'layer_type']


class NeuroglancerViewSerializer(serializers.ModelSerializer):
    lab_name = serializers.CharField(source='lab.lab_name')

    class Meta:
        model = NeuroglancerView
        fields = '__all__'
        ordering = ['id']


 
class NeuronSerializer(serializers.Serializer):
    """
    Serializes a list of brain atlas segment Ids
    Used for the Mouselight data
    """
    segmentId = serializers.ListField()

class AnatomicalRegionSerializer(serializers.Serializer):
    """
    Serializes a list of brain atlas region names
    Used for the Mouselight data
    """
    segment_names = serializers.ListField()

class ViralTracingSerializer(serializers.Serializer):
    """
    Serializes a list of tracing brain urls
    Used for the Mouselight data
    """
    brain_names = serializers.ListField()
    frac_injections = serializers.ListField()
    primary_inj_sites = serializers.ListField()
    brain_urls = serializers.ListField()
