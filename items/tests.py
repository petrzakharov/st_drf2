from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from items.models import Item
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
        [
            Item.objects.create(
                title=f"Item {b}",
                description=f"text {b}",
                weight=int(b),
                price=int(b)
            )
            for b in [100, 500]
        ]

    @classmethod
    def setUpTestData(cls):
        pass

    def test_list_item(self):
        self.url = reverse('items:item-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, {'price__lte': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '100.00')
        count_items = Item.objects.count()
        self.assertEqual(count_items, 2)
        item = Item.objects.filter(price=100)[0]
        self.assertEqual(model_to_dict(item)['price'], 100)
        response = self.client.get(self.url, {'price__gt': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '500.00')

    def test_detail_item(self):
        self.client.force_authenticate(self.user)
        item = Item.objects.get(price=100)
        self.url = reverse('items:item-detail', kwargs={'pk': item.id})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '100.00')
        self.assertEqual(model_to_dict(item)['price'], 100)





