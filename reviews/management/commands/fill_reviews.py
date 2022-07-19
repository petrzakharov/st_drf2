import requests

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Review
from users.models import User


class Command(BaseCommand):
    URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/reviews.json'
    STATUS_MAPPING = {
        'published': 'S',
        'hidden': 'D',
        'new': 'M'
    }

    def handle(self, *args, **options):
        response = requests.get(self.URL)
        if response.status_code == 200:
            result = response.json()
            for item in result:
                user = User.objects.get(pk=item['author'])
                Review.objects.create(
                    author=user,
                    text=item['content'],
                    created_at=item['created_at'],
                    published_at=item['published_at'],
                    status=self.STATUS_MAPPING[item['status']]
                )
        else:
            raise CommandError(f'Ошибка при загрузке данных, {response.status_code}')
