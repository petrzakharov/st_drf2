from django.db import models
from django.utils import timezone

from users.models import User


class Review(models.Model):
    STATUSES = (
        ('M', 'Moderation'),
        ('P', 'Published'),
        ('R', 'Rejected'),
    )
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='M')

    def save(self, *args, **kwargs):
        if self.status == 'P':
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
