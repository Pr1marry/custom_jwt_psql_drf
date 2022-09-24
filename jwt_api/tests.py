from unittest import TestCase

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import User


class MyTests(TestCase):
    def test_api_jwt(self):

        url = reverse('register')
        u = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        u.is_active = False
        u.save()

        resp = self.client.post(url, {'email': 'user@foo.com', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        u.is_active = True
        u.save()

        resp = self.client.post(url, {'username': 'user@foo.com', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        verification_url = reverse('api-jwt-verify')
        resp = self.client.post(verification_url, {'token': token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(verification_url, {'token': 'abc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        resp = client.get('/api/v1/account/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        client.credentials(HTTP_AUTHORIZATION='JWT' + token)
        resp = client.get('/api/v1/account/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
