from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='profuser', password='pass')
        self.client.force_authenticate(self.user)

    def test_get_profile(self):
        resp = self.client.get('/api/auth/profile/me/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('phone', data)

    def test_upload_avatar(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
        )
        avatar = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        resp = self.client.patch('/api/auth/profile/me/', {'avatar': avatar}, format='multipart')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('avatar', data)
from django.test import TestCase
from rest_framework.test import APIClient


class UsersAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login(self):
        resp = self.client.post('/api/auth/register/', {'username': 'tuser', 'password': 'testpass'})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn('token', data)

        # login
        resp2 = self.client.post('/api/auth/login/', {'username': 'tuser', 'password': 'testpass'})
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('token', resp2.json())
