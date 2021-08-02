from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Review, Title
from .serializers import CommentsSerializer, ReviewSerializer
from .permissions import IsAuthorModeratorOrAdmin


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorModeratorOrAdmin,
        IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):
        params = {
            'author': self.request.user,
            'title': get_object_or_404(
                Title, pk=self.kwargs.get('title_id')
            )
        }
        serializer.save(**params)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [
        IsAuthorModeratorOrAdmin,
        IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):
        params = {
            'author': self.request.user,
            'review': get_object_or_404(
                Review, pk=self.kwargs.get('review_id')
            )
        }
        serializer.save(**params)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()
