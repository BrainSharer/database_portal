from django import forms
from django.db.models import Max
from django.forms import ModelChoiceField
from brain.models import Animal, Slide, SlideCziToTif


class AnimalForm(forms.Form):
    prep_id = ModelChoiceField(label='Animal',
                               queryset=Animal.objects.all().order_by('prep_id'),
                               required=False,
                               widget=forms.Select(attrs={'onchange': 'id_list.submit();', 'class': 'form-control'}))

    class Meta:
        fields = ('prep_id',)


class AnimalChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.prep_id


# helper methods for the slide admin form

def repeat_scene(slide_id, inserts, scene_number):
    tifs = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True) \
        .filter(scene_number=scene_number)

    if not tifs:
        tifs = find_closest_neighbor(slide_id, scene_number)

    for insert in range(inserts):
        create_scene(tifs, scene_number)


def remove_scene(slide_id, deletes, scene_number):
    channels = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True).values('channel').distinct().count()
    tifs = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True) \
        .filter(scene_number=scene_number)
    scene_index = tifs[0].scene_index
    tifs = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True) \
        .filter(scene_index=scene_index).order_by('scene_number')[:deletes*channels]

    for tif in tifs:
        tif.delete()


def create_scene(tifs, scene_number):
    for tif in tifs:  #
        newtif = tif
        newtif.active = True
        newtif.pk = None
        newtif.scene_number = scene_number
        newtif.save()


def find_closest_neighbor(slide_id, scene_number):
    """
    Get the nearest scene. Look first at the preceding tifs, if nothing is there, go for the one just after
    :param slide_id:  primary key of the slide
    :param scene_number: scene number. 1 per set of 3 channels
    :return:  set of tifs
    """
    channels = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True).values('channel').distinct().count()
    below = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True) \
                .filter(scene_number__lt=scene_number).order_by('-scene_number')[:channels]
    if below.exists():
        tifs = below
    else:
        tifs = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True) \
                .filter(scene_number__gt=scene_number).order_by('scene_number')[:channels]

    return tifs


def set_scene_active(slide_id, scene_number):
    channels = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True).values('channel').distinct().count()
    active_tifs = SlideCziToTif.objects.filter(slide_id=slide_id)\
        .filter(active=True).filter(scene_number=scene_number).order_by('scene_number')[:channels]
    inactive_tifs = SlideCziToTif.objects.filter(slide_id=slide_id)\
        .filter(active=False).filter(scene_number=scene_number).order_by('scene_number')[:channels]
    for tif in active_tifs:
        tif.active = False
        tif.save()
    for tif in inactive_tifs:
        tif.active = True
        tif.save()

def set_scene_inactive(slide_id, scene_number):
    tifs = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True).filter(scene_number=scene_number)
    for tif in tifs:
        tif.active = False
        tif.save()


def set_end(slide_id, scene_number):
    tifs = SlideCziToTif.objects.filter(slide_id=slide_id).filter(scene_number__gte=scene_number)
    for tif in tifs:
        tif.active = False
        tif.save()


def scene_reorder(slide_id):
    # now get the order of scenes correct
    scenes_tifs = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True).order_by('scene_number')
    channels = SlideCziToTif.objects.filter(slide_id=slide_id).filter(active=True).values('channel').distinct().count()
    len_tifs = len(scenes_tifs) + 1
    flattened = [item for sublist in [[i] * channels for i in range(1, len_tifs)] for item in sublist]

    for new_scene, tif in zip(flattened, scenes_tifs):  # iterate over the scenes
        tif.scene_number = new_scene
        tif.save()


def save_slide_model(self, request, obj, form, change):
    scene_numbers = [1, 2, 3, 4, 5, 6]
    qc_1 = form.cleaned_data.get('scene_qc_1')
    qc_2 = form.cleaned_data.get('scene_qc_2')
    qc_3 = form.cleaned_data.get('scene_qc_3')
    qc_4 = form.cleaned_data.get('scene_qc_4')
    qc_5 = form.cleaned_data.get('scene_qc_5')
    qc_6 = form.cleaned_data.get('scene_qc_6')


    # do the QC fields
    OUTOFFOCUS = 1
    BADTISSUE = 2
    END = 3
    OK = 0
    qc_values = [qc_1, qc_2, qc_3, qc_4, qc_5, qc_6]
    current_qcs = Slide.objects.values_list('scene_qc_1', 'scene_qc_2', 'scene_qc_3',
                                            'scene_qc_4', 'scene_qc_5',
                                            'scene_qc_6').get(pk=obj.id)
    # this top loop needs to be run before the 2nd loop to make sure the required
    # tifs get set to inactive before finding a nearest neighbour
    for qc_value, current_qc, scene_number in zip(qc_values, current_qcs, scene_numbers):
        if qc_value in [OUTOFFOCUS, BADTISSUE] and qc_value != current_qc:
            set_scene_inactive(obj.id, scene_number)
    # tifs get set to active to back out a mistake
    for qc_value, current_qc, scene_number in zip(qc_values, current_qcs, scene_numbers):
        if qc_value == OK and qc_value != current_qc:
            set_scene_active(obj.id, scene_number)

    # taken out 15 jul 2021
    #for qc_value, current_qc, scene_number in zip(qc_values, current_qcs, scene_numbers):
    #    if qc_value in [OUTOFFOCUS, BADTISSUE] and qc_value != current_qc:
    #        tifs = find_closest_neighbor(obj.id, scene_number)
    #        create_scene(tifs, scene_number)

    for qc_value, current_qc, scene_number in zip(qc_values, current_qcs, scene_numbers):
        if qc_value == END and qc_value != current_qc:
            set_end(obj.id, scene_number)

    form_names = ['insert_before_one', 'insert_between_one_two', 'insert_between_two_three',
                  'insert_between_three_four', 'insert_between_four_five', 'insert_between_five_six']
    insert_values = [form.cleaned_data.get(name) for name in form_names]

    moves = sum([value for value in insert_values if value is not None])
    # scene_count = obj.scenes
    # scenes = range(1, scene_count + 1)
    ## do the inserts
    current_values = Slide.objects.values_list('insert_before_one', 'insert_between_one_two',
                                               'insert_between_two_three',
                                               'insert_between_three_four', 'insert_between_four_five',
                                               'insert_between_five_six').get(pk=obj.id)

    for new, current, scene_number in zip(insert_values, current_values, scene_numbers):
        if new is not None and new > current:
            difference = new - current
            repeat_scene(obj.id, difference, scene_number)
        if new is not None and new < current:
            difference = current - new
            remove_scene(obj.id, difference, scene_number)

    scene_reorder(obj.id)


    obj.scenes = SlideCziToTif.objects.filter(slide_id=obj.id).filter(channel=1).filter(active=True).count()

class TifInlineFormset(forms.models.BaseInlineFormSet):

    def save_existing(self, form, instance, commit=True):
        """
        This is called when updating an instance.
        """
        obj = super(TifInlineFormset, self).save_existing(form, instance, commit=False)
        ch23s = SlideCziToTif.objects.filter(slide_id=obj.slide_id).filter(scene_number=obj.scene_number).filter(scene_index=obj.scene_index)
        for ch23 in ch23s:
            ch23.active = False
            ch23.save()
        scene_reorder(obj.slide_id)
        if commit:
            obj.save()
        return obj

