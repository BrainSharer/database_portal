import os
from django import forms

from django.forms import ModelChoiceField
from brain.models import Animal, ScanRun
from neuroglancer.models import NeuroglancerModel
from neuroglancer.create_state_views import get_layer_type
from django.core.exceptions import ValidationError

class AnimalChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.animal


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

class NeuroglancerUpdateForm(forms.ModelForm):
    class Meta:
        model = NeuroglancerModel
        fields = ['comments']
    
    
class NeuroglancerModelForm(forms.ModelForm):
    animal = ModelChoiceField(label='Create main layer',
                            queryset=Animal.objects
                            .filter(active=True)
                            .order_by('animal'),
                            required=True,
                            widget=forms.Select(attrs={'class': 'form-control',
                                                       'style':'display:block;'}))
    PANELS=[('4panel','4panel'),
         ('xy','Upper left'),
         ('yz','Lower right'),
         ('xz','Upper right'),
         ('3d', '3D')]

    panels = forms.ChoiceField(choices=PANELS, widget=forms.RadioSelect)
    include_atlas = forms.ChoiceField(choices=[('yes','yes'),('no','no')], widget=forms.RadioSelect)
    
    class Meta:
        model = NeuroglancerModel
        fields = ['comments','panels', 'include_atlas', 'animal']

    def __init__(self, *args, **kwargs):
        #extra_fields = kwargs.pop('extra', 0)
        super().__init__(*args, **kwargs)
        self.fields['include_atlas'].initial = 'no'
        self.fields['comments'].label = 'Title of state'

    def clean(self):
        selected_states = self.data.get('selected_states')

        if selected_states is None:
            self.data = self.data.copy()
            self.data['animal'] = None
            raise ValidationError('You must select a title, and at least one layer.')
        
    def prepareModel(self, request, obj, form, change):
        state = {}
        for key, value in request.POST.items():
            print(f'Key: {key}')
            print(f'Value: {value}')
            print()
        if 'animal' in request.POST and 'selected_states' in request.POST:
            animal = request.POST['animal']
            panel = request.POST['panels']
            include_atlas = bool({'yes': True, 'no': False}[str(request.POST['include_atlas']).lower()])
            directories = request.POST.getlist('selected_states')
            layers, visible_layer = create_layers(directories, include_atlas)
            scan_run = ScanRun.objects.get(pk=animal)
            state['dimensions'] = {'x':[scan_run.resolution, 'um'],
                                   'y':[scan_run.resolution, 'um'],
                                   'z':[scan_run.zresolution, 'um'] }
            state['position'] = [scan_run.width / 2, scan_run.height / 2, 225]
            state['selectedLayer'] = {'visible': True, 'layer': visible_layer}
            state['crossSectionScale'] = 90
            state['projectionScale'] = scan_run.width
            state['layers'] = layers
            state['gpuMemoryLimit'] = 4000000000
            state['systemMemoryLimit'] = 8000000000
            state['layout'] = panel
            
        obj.neuroglancer_state = state
        obj.person = request.user
        return
        
        

def create_layers(directories, include_atlas):
    layers = []
    shaders = {}
    first_layer_name =  os.path.basename(os.path.normpath(directories[0]))
    create_atlas = False
    shaders[0] = '#uicontrol invlerp normalized\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n\nvoid main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n  \t  emitGrayscale(pix) ;\n}'
    shaders[1] = '#uicontrol invlerp normalized  (range=[0,45000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour) {\n  \t   emitRGB(vec3(pix,0,0));\n  \t} else {\n  \t  emitGrayscale(pix) ;\n  \t}\n\n}\n'
    shaders[2] = '#uicontrol invlerp normalized  (range=[0,5000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour){\n       emitRGB(vec3(0, (pix),0));\n    } else {\n      emitGrayscale(pix) ;\n    }\n\n}\n'
    for i, directory in enumerate(directories):
        layer_name = os.path.basename(os.path.normpath(directory))
        layer = {}
        layer['name'] = layer_name
        layer['shader'] = shaders.get(i, 0)
        layer['source'] = f'precomputed://{directory}'
        layer['type'] = get_layer_type(directory)
        layer['visible'] = True
        layers.append(layer)
    
    if include_atlas:
        atlas = create_atlas_layer()
        print('atlas', atlas)
        layers.append(atlas)
    return layers, first_layer_name


def create_atlas_layer():
        atlas = {}
        atlas['type'] = 'segmentation'
        atlas['source'] = 'precomputed://https://activebrainatlas.ucsd.edu/data/structures/atlasV7'
        atlas['tab'] = 'segments'
        atlas['segments'] = ['1', '2', '3','4', '5',
                             '6','7','8','9','10', 
                             '11', '12', '13','14', '15',
                             '16','17','18','19','20',
                             '21','22','23','24','25',
                             '26','27','28']
        atlas['name'] = 'atlasV7'
        
        return atlas
