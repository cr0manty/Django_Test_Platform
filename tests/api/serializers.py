from rest_framework import serializers

from tests.models import Test, UserTestPass


class TestSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.SlugRelatedField(many=False, slug_field="username", read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'slug', 'author',
                  'date_create', 'passes_number',
                  'description', 'questions', 'comments')


class UserTestResultSerializer(serializers.ModelSerializer):
    test = serializers.SlugRelatedField(many=False, slug_field="name", read_only=True)
    user = serializers.SlugRelatedField(many=False, slug_field="username", read_only=True)

    class Meta:
        model = UserTestPass
        fields = ('id', 'test', 'user', 'correct_answer',
                  'amount_answer', 'correct_present')
