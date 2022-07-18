from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from reviews.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    is_published = SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'author', 'status', 'text', 'created_at', 'published_at', 'is_published')

    @staticmethod
    def get_is_published(obj):
        if obj.published_at is not None:
            return True
        return False
