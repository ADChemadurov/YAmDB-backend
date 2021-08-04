from django.contrib.auth.models import AbstractUser
from django.db import models


class YamdbUser(AbstractUser):

    class UserRolesChices(models.TextChoices):
        USER = 'user',
        MODERATOR = 'moderator',
        ADMIN = 'admin'

    email = models.EmailField(blank=False, unique=True)
    bio = models.CharField(
        max_length=200,
        verbose_name='О себе',
        help_text=('Введите информацию о себе, '
                   'своих интересах и предпочтениях.'),
        blank=True,
    )

    role = models.CharField(
        max_length=15,
        choices=UserRolesChices.choices,
        default='user',
    )
    confirmation_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    REQUIRED_FIELDS = ['email']
