from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .serializers import TestSerializer
from tests.models import Test


class AllTestsViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('name')
    serializer_class = TestSerializer

