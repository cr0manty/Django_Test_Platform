from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .serializers import TestSerializer, UserTestResultSerializer
from tests.models import Test, UserTestPass


class AllTestsViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().order_by('id')
    serializer_class = TestSerializer


class AllTestsResultViewSet(viewsets.ModelViewSet):
    queryset = UserTestPass.objects.all()
    serializer_class = UserTestResultSerializer
