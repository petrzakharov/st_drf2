from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews.models import Review
from users.models import User


class ReviewTestCase(APITestCase):
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
        self.review_text = 'Good review about something'

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('reviews:general-viewset')

    def test_post_review(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {'text': self.review_text})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], self.review_text)
        review = Review.objects.get()
        self.assertEqual(model_to_dict(review)['text'], self.review_text)
        self.assertEqual(model_to_dict(review)['status'], 'M')

    def test_list_review(self):
        self.client.force_authenticate(self.user)
        Review.objects.create(author=self.user, text=self.review_text, status='P')
        review = Review.objects.get()
        print(review.status)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(model_to_dict(review)['text'], self.review_text)
        self.assertEqual(response.data['results'][0]['text'], self.review_text)
