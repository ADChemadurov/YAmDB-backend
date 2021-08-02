from rest_framework import serializers

from .models import Comments, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        exclude = ['title', ]
        model = Review

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if (Review.objects.filter(author=user, title_id=title_id).exists()
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments
