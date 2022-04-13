import json
from rest_framework import status
from django.test import Client, TransactionTestCase
# Create your tests here.
from authentication.models import User, Lab
from brain.models import Animal, Biocyc, BrainAtlas
from neuroglancer.models import NeuroglancerModel, AnnotationPoints, BrainRegion
from random import uniform
import os
from datetime import datetime


class TestNeuroglancerModel(TransactionTestCase):
    client = Client()

    def setUp(self):
        self.comments = 'XXX'
        self.username = 'edward'
        self.animal_name = 'DK39'
        self.lab_name = 'UCSD'
        self.lab_url = 'https://activebrainatlas.ucsd.edu'
        self.bio_name = 'mouse'
        #biocyc
        try:
            query_set = Biocyc.objects.filter(bio_name=self.bio_name)
        except Biocyc.DoesNotExist:
            self.biocyc = None
        if query_set is not None and len(query_set) > 0:
            self.biocyc = query_set[0]
        else:
            self.biocyc = Biocyc.objects.create(bio_name=self.bio_name)
        #lab
        try:
            query_set = Lab.objects.filter(lab_name=self.lab_name)
        except Lab.DoesNotExist:
            self.lab = None
        if query_set is not None and len(query_set) > 0:
            self.lab = query_set[0]
        else:
            self.lab = Lab.objects.create(
                lab_name=self.lab_name, lab_url=self.lab_url)
        #user
        try:
            query_set = User.objects.filter(username=self.username)
        except User.DoesNotExist:
            self.owner = None
        if query_set is not None and len(query_set) > 0:
            self.owner = query_set[0]
        else:
            self.owner = User.objects.create(username=self.username,
                                             email='super@email.org',
                                             password='pass',
                                             lab=self.lab)
        # animal
        try:
            query_set = Animal.objects.filter(animal_name=self.animal_name)
        except Animal.DoesNotExist:
            self.animal = None
        if query_set is not None and len(query_set) > 0:
            self.animal = query_set[0]
        else:
            self.animal = Animal.objects.create(animal_name=self.animal_name,
                                                lab=self.lab, biocyc=self.biocyc)
        # brain_atlas
        self.atlas = 'Allen'
        try:
            query_set = BrainAtlas.objects.filter(atlas_name=self.atlas)
        except BrainAtlas.DoesNotExist:
            self.brain_region = None
        if query_set is not None and len(query_set) > 0:
            self.brain_atlas = query_set[0]
        else:
            self.brain_atlas = BrainAtlas.objects.create(atlas_name=self.atlas)
        # brain_region
        try:
            query_set = BrainRegion.objects.filter(abbreviation='point')
        except BrainRegion.DoesNotExist:
            self.brain_region = None
        if query_set is not None and len(query_set) > 0:
            self.brain_region = query_set[0]
        else:
            self.brain_region = BrainRegion.objects.create(
                abbreviation='point', brain_atlas=self.brain_atlas)

    def test_neuroglancer_url(self):
        response = self.client.get("/neuroglancer")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_annotations_url(self):
        label = 'XXX'
        x1 = uniform(0, 65000)
        y1 = uniform(0, 35000)
        z1 = uniform(0, 450)
        try:
            p = AnnotationPoints.objects.create(animal=self.animal,
                                                brain_region=self.brain_region,
                                                label=label, owner=self.owner,
                                                x=x1, y=y1, z=z1)
        except Exception as e:
            print('could not create', e)
        try:
            p.save()
        except Exception as e:
            print('could not save', e)

        response = self.client.get("/annotations")
        self.assertGreater(
            len(response.data), 0, msg="The number of annotations should be greater than 0.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_annotation(self):
        """
        Description of test_create_annotation

        Args:
            self (undefined):

        """
        n = 10
        for _ in range(n):
            x = uniform(0, 65000)
            y = uniform(0, 35000)
            z = uniform(0, 450)
            p = AnnotationPoints.objects.create(animal=self.animal, brain_region=self.brain_region,
                                                label='COM', owner=self.owner, x=x, y=y, z=z)
            p.save()

        c = AnnotationPoints.objects.count()
        self.assertGreaterEqual(
            c, n, msg=f'Error: Annotation point table has less than {n} entries.')

    def test_annotation_url(self):
        """
        Description of test_annotation_url

        Args:
            self (undefined):

        """
        label = 'premotor'
        n = 10
        for _ in range(n):
            x = uniform(0, 65000)
            y = uniform(0, 35000)
            z = uniform(0, 450)
            p = AnnotationPoints.objects.create(animal=self.animal, brain_region=self.brain_region,
                                                label=label, owner=self.owner, x=x, y=y, z=z)
            p.save()
        c = AnnotationPoints.objects\
            .filter(animal=self.animal)\
            .filter(label=label)\
            .count()
        url = f'/annotation/{self.animal.id}/{label}'
        response = self.client.get(url)
        self.assertGreaterEqual(len(
            response.data), c, msg="The number of annotations entered and returned do not match.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_get_state(self):
        '''
        Ensure we can create a new neuroglancer_state object.
        neuroglancer_state is the new, url is the old
        owner is the new, person_id is the old
        '''
        # clear object from DB just in case
        NeuroglancerModel.objects.filter(comments=self.comments).delete()
        parent_path = os.getcwd()
        jfile = f'{parent_path}/scripts/363.json'
        state = json.load(open(jfile))
        fields = ['url', 'owner', 'comments', 'id', 'created']

        data = {}
        data['neuroglancer_state'] = json.dumps(state)
        data['user_date'] = '999999'
        data['comments'] = self.comments
        data['FK_owner_id'] = self.owner.id
        data['created'] = datetime.now()
        data['updated'] = datetime.now()
        data['lab'] = self.lab

        response = self.client.post('/neuroglancer', data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('ERROR', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """
        neuroglancerModel = NeuroglancerModel.objects.filter(comments=self.comments)
        n = NeuroglancerModel.objects.filter(comments=self.comments).count()
        self.assertEqual(n, 1)
        self.assertEqual(neuroglancerModel[0].comments, self.comments)
        self.state_id = neuroglancerModel[0].id
        url = "/neuroglancer/" + str(self.state_id)
        response = self.client.get(url)
        for field in fields:
            if field not in response.data:
                print(f'{field} is not in response.data')
        self.assertGreater(len(response.data), 1, msg="Get neuroglancer did not return valid data.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """
