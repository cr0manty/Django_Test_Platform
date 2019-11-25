from rest_framework import serializers, status
from django.db.models import Q
from rest_framework.response import Response

from home.models import User
from tests.models import Test, Comment, UserTestPass


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )
    lookup_field = 'username'

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'is_staff', 'date_joined',
                  'birth_date', 'about', 'image')
        read_only_fields = ('id', 'is_staff', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class UserCommentsSerializer(serializers.ModelSerializer):
    test = serializers.SlugRelatedField(many=False, slug_field="name", read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'test', 'date_create', 'text')
        read_only_fields = ('test', 'date_create')

    def update(self, instance, validated_data):
        pass


class UserTestSerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'slug', 'date_create',
                  'passes_number', 'description',
                  'questions', 'comments')


class UserTestResultSerializer(serializers.ModelSerializer):
    test = serializers.SlugRelatedField(many=False, slug_field="name", read_only=True)

    class Meta:
        model = UserTestPass
        fields = ('id', 'test', 'correct_answer',
                  'amount_answer', 'correct_present')

