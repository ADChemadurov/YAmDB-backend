from rest_framework import serializers

from .models import YamdbUser


class ListUsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'first_name', 'last_name', 'username', 'bio', 'email', 'role',
        ]
        model = YamdbUser
