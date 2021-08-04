from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import SET_NULL

from auth_users.models import YamdbUser

User = YamdbUser


class Category(models.Model):
    name = models.CharField('Название Категории', max_length=50)
    slug = models.SlugField('Ссылка на содержимое Категории',
                            unique=True,
                            blank=True,
                            max_length=50,
                            auto_created=True)

    class Meta:
        ordering = ('name',)
        UniqueConstraint(fields=['slug'], name='unique_slug_constraint')

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField('Название Жанра', max_length=50)
    slug = models.SlugField('Ссылка на список произведений конкретного Жанра',
                            unique=True,
                            blank=True,
                            max_length=50,
                            auto_created=True)

    class Meta:
        ordering = ('name',)
        UniqueConstraint(fields=['slug'], name='unique_slug_constraint')

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField('Название Произведения', max_length=100)
    year = models.IntegerField('Год выхода Произведения',
                               validators=[
                                   MaxValueValidator(date.today().year),
                                   MinValueValidator(-900)
                               ])
    description = models.TextField('Описание Произведения')
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category,
                                 on_delete=SET_NULL,
                                 null=True,
                                 help_text='Категория Произведения',
                                 related_name='title')

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name
