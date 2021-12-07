import os
from django import forms

from django.forms import ModelChoiceField
from brain.models import Animal, ScanRun
from neuroglancer.models import NeuroglancerModel
from neuroglancer.create_state_views import get_layer_type
from django.core.exceptions import ValidationError

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
        exclude = ['prep', 'structure', 'person', 'input_type',
            'x', 'y', 'section', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['layer'].queryset = LayerData.objects.all()
        self.fields['layer'].options = {'one':1, 'two':2}
    
    
class NeuroglancerModelForm(forms.ModelForm):
    animal = ModelChoiceField(label='Create main layer',
                            queryset=Animal.objects
                            .filter(active=True)
                            .order_by('prep_id'),
                            required=True,
                            widget=forms.Select(attrs={'class': 'form-control',
                                                       'style':'display:block;'}))
    states = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = NeuroglancerModel
        fields = ['comments', 'animal']

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)
        super().__init__(*args, **kwargs)
        self.fields['states'].initial = extra_fields
        self.fields['comments'].label = 'Title of state'

    def clean(self):
        cleaned_data = super().clean()
        states = cleaned_data.get("selected_states")

        if states is None:
            self.data = self.data.copy()
            self.data['animal'] = None
            raise ValidationError("You must select a title, and at least one layer.")
        
    def prepareModel(self, request, obj, form, change):
        state = {}
        if 'animal' in request.POST and 'selected_states' in request.POST:
            animal = request.POST['animal']
            directories = request.POST.getlist("selected_states")
            scan_run = ScanRun.objects.get(prep__prep_id=animal)
            state['dimensions'] = {'x':[scan_run.resolution, "um"],
                                   'y':[scan_run.resolution, "um"],
                                   'z':[scan_run.zresolution, "um"] }
            state['position'] = [scan_run.width / 2, scan_run.height / 2, 225]
            state['projectionScale'] = scan_run.width
            state['crossSectionScale'] = 90
            state['layout'] = '4panel'
            state['selectedLayer'] = {'visible':'true'}
            layers = create_layers(directories)
            state['layers'] = layers
            
        obj.neuroglancer_state = state
        obj.person = request.user
        return
        
        

def create_layers(directories):
    layers = []
    shaders = {}
    shaders[0] = "#uicontrol invlerp normalized\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n\nvoid main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n  \t  emitGrayscale(pix) ;\n}"
    shaders[1] = "#uicontrol invlerp normalized  (range=[0,45000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour) {\n  \t   emitRGB(vec3(pix,0,0));\n  \t} else {\n  \t  emitGrayscale(pix) ;\n  \t}\n\n}\n"
    shaders[2] = "#uicontrol invlerp normalized  (range=[0,5000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour){\n       emitRGB(vec3(0, (pix),0));\n    } else {\n      emitGrayscale(pix) ;\n    }\n\n}\n"
    for i, directory in enumerate(directories):
        layer_name = os.path.basename(os.path.normpath(directory))
        layer = {}
        layer["name"] = layer_name
        layer["shader"] = shaders.get(i, 0)
        layer["source"] = f"precomputed://{directory}"
        layer["type"] = get_layer_type(directory)
        layer["visible"] = True
        layers.append(layer)
    return layers

