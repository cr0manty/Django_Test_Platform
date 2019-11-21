from rest_framework import serializers

from home.models import User
from tests.models import Test, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'is_staff', 'date_joined',
                  'birth_date', 'about', 'image')


class UserCommentsSerializer(serializers.ModelSerializer):
    test = serializers.SlugRelatedField(many=False, slug_field="name", read_only=True)

    class Meta:
        model = Comment
        fields = ( 'date_create', 'text')


class UserTestSerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('name', 'slug', 'date_create',
                  'passes_number', 'description',
                  'questions', 'comments')
