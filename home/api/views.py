from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *


class AllUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class UserInfoAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        serializer = UserSerializer(user)
        return Response(serializer.data)


# TODO
class UserCommentsAPI(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        comments = Comment.objects.filter(author__username=username).all()
        serializer = UserCommentsSerializer(comments)
        return Response(serializer.data)


class UserTestsAPI(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        tests = Test.objects.filter(author__username=username).all()
        serializer = UserTestSerializer(tests)
        return Response({'tests': serializer.data})
