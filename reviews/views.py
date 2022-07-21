from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewsViewset(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user, status='P').select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
