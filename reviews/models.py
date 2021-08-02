from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from auth_users.models import YamdbUser
from categories.models import Title

User = YamdbUser


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    text = models.TextField()


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
