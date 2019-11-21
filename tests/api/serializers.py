from rest_framework import serializers

from tests.models import Test


class TestSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.SlugRelatedField(many=False, slug_field="username", read_only=True)

    class Meta:
        model = Test
        fields = ('name', 'slug', 'author', 'date_create',
                  'passes_number', 'description',
                  'questions', 'comments')
