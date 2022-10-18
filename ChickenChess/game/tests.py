from urllib import response
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import Pending_Game

# Create your tests here.
class CreateGameTest(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_GetCreatePending_game(self):
        response = self.client.get(reverse('game:creategame'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/creategameView.html')

    def test_PostPendingGameRegular(self):
        response = self.client.post(reverse('game:creategame'),
        {
            'inviting_color' : 'white',
            'time' : 1,
            'increment' : 1
        }
        )
        self.assertEquals(response.status_code,302)

    def test_PostPending_negative_time(self):
        response = self.client.post(reverse('game:creategame'),
        {
            'inviting_color' : 'black',
            'time' : -1,
            'increment' : 1
        }
        )
        self.assertEquals(response.status_code,404)
    
    def test_PostPending_negative_increment(self):
        response = self.client.post(reverse('game:creategame'),
        {
            'inviting_color' : 'black',
            'time' : 1,
            'increment' : -1
        }
        )
        self.assertEquals(response.status_code,404)
    
    def test_PostPending_non_numerical_time(self):
        response = self.client.post(reverse('game:creategame'),
        {
            'inviting_color' : 'black',
            'time' : 'infinite',
            'increment' : 'laughing'
        }
        )
        self.assertEquals(response.status_code,404)