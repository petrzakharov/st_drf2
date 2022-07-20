from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class RegisterUserTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('users:register')

    def test_register_user(self):
        data = {
            'address': 'Test Address',
            'phone': '123456789',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'email': 'user_test@email.com',
            'password': 'TestUser12345678'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        # user = User.objects.get()
        # self.assertEqual(model_to_dict(user), {**data})


class ListUserTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'address': 'Test Address',
            'phone': '123456789',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'email': 'user_test@email.com',
            'password': 'TestUser12345678'
        }
        self.user = User.objects.create(**self.data)

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('users:general-viewset')

    def test_get_current_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.data['email'])
        user = User.objects.get()
        self.assertEqual(model_to_dict(user)['email'], self.data['email'])
        self.assertEqual(model_to_dict(user)['last_name'], self.data['last_name'])
        self.assertEqual(model_to_dict(user)['first_name'], self.data['first_name'])

    def test_put_current_user(self):
        self.client.force_authenticate(self.user)
        self.data['email'] = 'new_user_email@yandex.ru'
        self.data['first_name'] = 'New User First Name'
        response = self.client.put(self.url, data=self.data)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.data['email'])
        self.assertEqual(response.data['first_name'], self.data['first_name'])
        self.assertEqual(model_to_dict(user)['first_name'], self.data['first_name'])

    def test_patch_current_user(self):
        self.client.force_authenticate(self.user)
        new_email = 'new_user_email@yandex.ru'
        new_first_name = 'New User First Name'
        response = self.client.patch(self.url, {'email': new_email, 'first_name': new_first_name})
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], new_email)
        self.assertEqual(model_to_dict(user)['email'], new_email)
