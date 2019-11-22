from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *


class AllUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class UserInfoAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserCommentsAPI(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        comments = Comment.objects.filter(author__username=username).all().order_by('id')
        serializer = UserCommentsSerializer(comments, many=True)
        return Response({username: {'comments': serializer.data}})

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username')


class UserCommentAPI(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        comment_id = self.kwargs.get('id')

        comment = get_object_or_404(Comment, author__username=username, id=comment_id)
        serializer = UserCommentsSerializer(comment)
        return Response({username: serializer.data})

    def delete(self, request, pk, format=None):
        username = self.kwargs.get('username')
        comment_id = self.kwargs.get('id')

        comment = get_object_or_404(Comment, author__username=username, id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        username = self.kwargs.get('username')
        comment_id = self.kwargs.get('id')
        comment = get_object_or_404(Comment, username=username, id=comment_id)

        comment.text = request.data.get('text', comment.text)
        comment.save()
        serializer = UserCommentsSerializer(comment)
        return Response({username: serializer.data})


class UserTestsCreateAPI(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        tests = Test.objects.filter(author__username=username).all().order_by('id')
        serializer = UserTestSerializer(tests, many=True)
        return Response({username: {'tests': serializer.data}})


class UserTestsPassAPI(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        tests_pass = UserTestPass.objects.filter(user__username=username).all().order_by('id')
        serializer = UserTestResultSerializer(tests_pass, many=True)
        return Response({username: {'pass': serializer.data}})
