from django.db import models

from users.models import User


class Review(models.Model):
    STATUSES = (
        ('M', 'Moderation'),
        ('S', 'Success'),
        ('D', 'Declined'),
    )
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUSES)
