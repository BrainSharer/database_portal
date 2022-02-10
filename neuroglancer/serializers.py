from rest_framework import serializers
from rest_framework.exceptions import APIException
import logging

from brain.models import BrainRegion
from neuroglancer.models import AnnotationPoints, NeuroglancerModel
from neuroglancer.atlas import update_annotation_data
from authentication.models import User

logging.basicConfig()
logger = logging.getLogger('django')


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
    animal_id = serializers.IntegerField()
    animal_name = serializers.CharField()
    label = serializers.CharField()
    input_type = serializers.CharField()
    FK_input_id = serializers.IntegerField()


class BrainRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrainRegion
        fields = '__all__'


class AnnotationPointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationPoints
        fields = '__all__'


class NeuroglancerSerializer(serializers.ModelSerializer):
    """Override method of entering a neuroglancer_state into the DB.
    The neuroglancer_state can't be in the NeuroglancerModel when it is returned
    to neuroglancer as it crashes neuroglancer."""
    owner_id = serializers.IntegerField()
    lab = serializers.CharField()

    class Meta:
        model = NeuroglancerModel
        fields = '__all__'
        ordering = ['-created']

    def create(self, validated_data):
        """
        This gets called when a user clicks New in Neuroglancer
        """
        logger.debug("validated_data:")
        logger.debug(validated_data)
        neuroglancerModel = NeuroglancerModel(
            neuroglancer_state=validated_data['neuroglancer_state'],
            user_date=validated_data['user_date'],
            comments=validated_data['comments'],
        )
        if 'owner_id' in validated_data:
            try:
                authUser = User.objects.get(pk=validated_data['owner_id'])
                logger.debug("auth user:")
                logger.debug(authUser)
                neuroglancerModel.owner = authUser
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
        if 'owner_id' in validated_data:
            try:
                authUser = User.objects.get(pk=validated_data['owner_id'])
                instance.owner = authUser
            except User.DoesNotExist:
                logger.error('Owner was not in validated data')
        try:
            instance.save()
        except APIException:
            logger.error('Could not save Neuroglancer model')
        update_annotation_data(instance)
        instance.neuroglancer_state = None
        return instance
    
class NeuronSerializer(serializers.Serializer):
    """
    Serializes a list of brain atlas segment Ids
    """
    segmentId = serializers.ListField()

class AnatomicalRegionSerializer(serializers.Serializer):
    """
    Serializes a list of brain atlas region names
    """
    segment_names = serializers.ListField()

class ViralTracingSerializer(serializers.Serializer):
    """
    Serializes a list of tracing brain urls
    """
    brain_names = serializers.ListField()
    frac_injections = serializers.ListField()
    primary_inj_sites = serializers.ListField()
    brain_urls = serializers.ListField()