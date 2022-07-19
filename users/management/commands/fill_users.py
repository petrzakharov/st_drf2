import requests

from django.core.management.base import BaseCommand, CommandError

from users.models import User


class Command(BaseCommand):
    URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/recipients.json'

    def handle(self, *args, **options):
        response = requests.get(self.URL)
        if response.status_code == 200:
            result = response.json()
            for item in result:
                username = item['email'].split('@')[0]
                User.objects.create(
                    first_name=item['info']['name'],
                    last_name=item['info']['surname'],
                    middle_name=item['info']['patronymic'],
                    phone=item['contacts']['phoneNumber'],
                    address=item['city_kladr'],
                    email=item['email'],
                    password=item['password'],
                    username=username,
                    id=item['id'],
                )
        else:
            raise CommandError(f'Ошибка при загрузке данных, {response.status_code}')
