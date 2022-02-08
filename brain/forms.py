from django import forms
from django.forms import ModelChoiceField
from brain.models import Animal


class AnimalForm(forms.Form):
    animal = ModelChoiceField(label='Animal',
                               queryset=Animal.objects.all().order_by('animal'),
                               required=False,
                               widget=forms.Select(attrs={'onchange': 'id_list.submit();', 'class': 'form-control'}))

    class Meta:
        fields = ('animal',)


class AnimalChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.animal

