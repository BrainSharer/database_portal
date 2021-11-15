from django import forms
from django.forms import ModelChoiceField
from brain.models import Animal

class PipelineForm(forms.Form):
    animal = ModelChoiceField(label='Animal',
                            queryset=Animal.objects.filter(active=True).all().order_by('prep_id'),
                            required=True,
                            widget=forms.Select(attrs={'onchange': 'id_list.submit();', 'class': 'form-control'}))
    class Meta:
        fields = ('prep_id',)
