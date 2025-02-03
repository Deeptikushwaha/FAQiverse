from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
