from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', )
    search_fields = ('name', )
    list_filter = ('id', )
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', )
    search_fields = ('name', )
    list_filter = ('id', )
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    search_fields = ('id', 'name', 'year', 'category')
    list_filter = ('year', )
    empty_value_display = '-пусто-'
