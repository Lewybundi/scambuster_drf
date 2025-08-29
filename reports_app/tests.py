from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from  reports_app import models

class ScamPostsListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Admin',password='1234')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.scamPosts= models.ScamPost.objects.create(
                                                scammer_name="Test Scammer",
                                                incidence_description="Test description",
                                                socials=["twitter.com/scammer"],
                                                isglobal=True)
    def test_scampost_create(self):
        data ={
        "scammer_name":"Test Scammer",
         "incidence_description":"Test description",
          "isglobal":True
        }
        response = self.client.post(reverse("reports"),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    def test_ScamPostsList_list(self):
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_ScamPost_id(self):
        response = self.client.get(reverse("report",args=(self.scamPosts.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_scampost_update(self):
        data= {
        "scammer_name":"Test Scammer",
        "incidence_description":"Test description-updated",
        "isglobal":True 
        }
        response =self.client.put(reverse("report",args=(self.scamPosts.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class SupportTestCase(APITestCase):
    def setUp(self):
       self.user = User.objects.create(username="Admin",password="1234")
       self.token = Token.objects.get(user__username=self.user)
       self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
       self.scampost = models.ScamPost.objects.create(
            scammer_name="Test Scammer",
            incidence_description="Test description"
        )
       self.support = models.SupportPost.objects.create(description="Testing",evidence_link="http://testing.com",scampost=self.scampost)
    def test_support_create(self):
        data ={
        "description":"Testing",
         "evidence_link":"http://testing.com"
        }
        response = self.client.post(reverse("support_create",args=(self.scampost.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    def test_support_list(self):
        response = self.client.get(reverse("supports"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        