import os
from datetime import datetime
import json

from rest_framework import status
from django.test import Client, TransactionTestCase
from authentication.models import User
# Create your tests here.
from neuroglancer.models import NeuroglancerModel

class TestNeuroglancerModel(TransactionTestCase):
    client = Client()
    

    def setUp(self):
        '''
        This method gets run every test below.
        '''
        self.layer_name = "TEST999"
        self.state_id = 0
    
    def test_neuroglancer_url(self):
        response = self.client.get("/neuroglancer")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_annotations_url(self):
        response = self.client.get("/annotations")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_annotation_url(self):
        response = self.client.get("/annotation/DK39/premotor/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_create_post_get_state(self):
        """
        Ensure we can create a new neuroglancer_state object.
        """
        
        self.super_user = User.objects.create_superuser(username='super',
                                                   email='super@email.org',
                                                   password='pass')
        
        parent_path = os.getcwd()
        jfile = f'{parent_path}/scripts/363.json'
        state = json.load(open(jfile))
        
        
        data = {}
        data['neuroglancer_state'] = json.dumps(state)
        data['user_date'] = '999999'
        data['comments'] = self.layer_name
        data['owner_id'] = self.super_user.id
        data['created'] = datetime.now()
        data['updated'] =  datetime.now()
        
        response = self.client.post('/neuroglancer', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NeuroglancerModel.objects.count(), 1)
        self.assertEqual(NeuroglancerModel.objects.get().comments, self.layer_name)
        self.state_id = NeuroglancerModel.objects.get().id
        
        response = self.client.get("/neuroglancer/" + str(self.state_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_post_get_update_get_state(self):
        """
        Ensure we can create, post, get, update and get again a 
        neuroglancer_state object.
        """
        
        self.super_user = User.objects.create_superuser(username='super',
                                                   email='super@email.org',
                                                   password='pass')
        
        parent_path = os.getcwd()
        jfile = f'{parent_path}/scripts/363.json'
        state = json.load(open(jfile))
        
        
        data = {}
        data['neuroglancer_state'] = json.dumps(state)
        data['user_date'] = '999999'
        data['comments'] = self.layer_name
        data['owner_id'] = self.super_user.id
        data['created'] = datetime.now()
        data['updated'] =  datetime.now()
        
        #post
        response = self.client.post('/neuroglancer', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NeuroglancerModel.objects.count(), 1)
        self.assertEqual(NeuroglancerModel.objects.get().comments, self.layer_name)
        self.state_id = NeuroglancerModel.objects.get().id
        
        #get
        response = self.client.get("/neuroglancer/" + str(self.state_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_comment_name = 'New comment name'
        data['comments'] = new_comment_name
        #update
        response = self.client.put('/neuroglancer/' + str(self.state_id), data, 
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(NeuroglancerModel.objects.count(), 1)
        self.assertEqual(NeuroglancerModel.objects.get().comments, new_comment_name)
        self.assertEqual(NeuroglancerModel.objects.get().id, self.state_id)
