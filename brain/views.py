from brain.models import Animal
from django.http import Http404
from rest_framework import views
from rest_framework.response import Response
from brain.serializers import AnimalSerializer

class AnimalList(views.APIView):
    """
    List all animals. No creation at this time.
    """
    def get(self, request, format=None):
        animals = Animal.objects.filter(active=True).order_by('animal')
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)

    """
    def post(self, request, format=None):
        serializer = AnimalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """

class AnimalDetail(views.APIView):
    """
    Retrieve only, no update or deletes.
    """
    def get_object(self, pk):
        try:
            return Animal.objects.get(pk=pk)
        except Animal.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        animal = self.get_object(pk)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)

    """
    def put(self, request, pk, format=None):
        animal = self.get_object(pk)
        serializer = AnimalSerializer(animal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        animal = self.get_object(pk)
        animal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """