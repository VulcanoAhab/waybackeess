from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from doCatalogue.docs.models import Doc
from doCatalogue.docs.serializers import DocSerializer

class DocViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows docs metadata to be viewed or edited.
    """
    queryset = Doc.objects.all().order_by('-created_at')
    serializer_class = DocSerializer
