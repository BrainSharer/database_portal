from rest_framework import serializers
from brain.models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['prep_id', ]