from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import YamdbUser


class UserCreationForm(forms.ModelForm):
    """
    Переопределяет форму создания пользователя, добавляет в нее поля:
    email, bio, role. Поля password1, password2 необходимо указать иначе
    они не будут отражаться в представлении.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )

    class Meta:
        model = YamdbUser
        fields = ('email', 'bio', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords dont match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Переопределяет форму изменения пользователя, добавляя в нее поля
    из fields.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = YamdbUser
        fields = ('username', 'email', 'bio', 'role',)

    def clean_password(self):
        return self.initial['password']


class YamdbUserAdmin(UserAdmin):
    """ Кастомная модель пользователя. """
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'bio', 'role', 'confirmation_code')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Роли', {'fields': ('role',)}),
        ('О пользователе', {'fields': ('bio',)}),
    )
    add_fieldsets = (
        (None, {'fields': (
            'username', 'email', 'password1', 'password2', 'role', 'bio',),
        }),
    )


admin.site.register(YamdbUser, YamdbUserAdmin)
