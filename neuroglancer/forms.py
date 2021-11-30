from django import forms
from django.forms import ModelChoiceField
from brain.models import Animal, ScanRun
from neuroglancer.models import NeuroglancerModel


class AnimalChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.prep_id


class LayerForm(forms.ModelForm):
    neuroglancerModels = ModelChoiceField(label='Annotation Layer',
                            queryset=NeuroglancerModel.objects.all().order_by('comments'),
                            required=True,
                            widget=forms.Select(attrs={'onchange': 'layerdata_form.submit();', 'class': 'form-control'}))

    class Meta:
        model = NeuroglancerModel
        exclude = ['prep', 'structure', 'person', 'url', 'transformation', 'input_type',
            'x', 'y', 'section', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['layer'].queryset = LayerData.objects.all()
        self.fields['layer'].options = {'one':1, 'two':2}
    
    
class NeuroglancerModelForm(forms.ModelForm):
    LAYERS = (
                ('', 'Select'),
                ('image', 'Image layer'),
                ('segment', 'Segmentation layer'),
                ('skeleton', 'Skeleton layer'),
                ('annotation', 'Annotation layer'),
            )
    layers = forms.ChoiceField(choices=LAYERS, label="Add layer", required=False)
    animals = ModelChoiceField(label='Create main layer',
                            queryset=Animal.objects.filter(active=True).order_by('prep_id'),
                            required=True,
                            widget=forms.Select(attrs={'class': 'form-control',
                                                       'style':'display:block;'}))

    class Meta:
        model = NeuroglancerModel
        fields = ['comments', 'person', 'animals', 'layers']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comments'].label = 'Title of state'
        # self.fields['layer'].queryset = LayerData.objects.all()
        # self.fields['layer'].options = {'one':1, 'two':2}
        
    def prepareModel(self, request, obj, form, change):
        state = {}
        scan_run = ScanRun.objects.get(prep__prep_id='DK52')
        state['dimensions'] = {'x':[scan_run.resolution, "um"],
                               'y':[scan_run.resolution, "um"],
                               'z':[scan_run.zresolution, "um"] }
        state['position'] = [scan_run.width / 2, scan_run.height / 2, 225]
        state['projectionScale'] = scan_run.width
        state['layers'] = []
        obj.neuroglancer_state = state
        
