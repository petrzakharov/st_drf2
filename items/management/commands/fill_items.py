import shutil

from django.core.management.base import BaseCommand, CommandError
import requests
from items.models import Item


class Command(BaseCommand):
    URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'
    SAVE_IMAGE_PATH = 'media/pictures/'

    @staticmethod
    def download_images(url, path):
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
        else:
            print(f'Не может быть загружено: {url}\n')

    def handle(self, *args, **options):
        response = requests.get(self.URL)
        if response.status_code == 200:
            result = response.json()
            for item in result:
                image_path = self.SAVE_IMAGE_PATH + str(item['id']) + '.jpg'
                self.download_images(item['image'], path=image_path)
                Item.objects.create(
                    title=item['title'],
                    description=item['description'],
                    image=image_path,
                    weight=item['weight_grams'],
                    price=item['price']
                )
        else:
            raise CommandError(f'Ошибка при сохранении объекта, {response.status_code}')
