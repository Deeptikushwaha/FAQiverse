from django.shortcuts import render

# Create your views here.    faq api views and 
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import FAQ
from .serializers import FAQSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

# views.py
from django.shortcuts import render
from .models import FAQ
from .cache_utils import get_translation_stats

def faq_dashboard(request):
    faqs = FAQ.objects.all()
    stats = get_translation_stats()
    
    context = {
        'faqs': faqs,
        'stats': stats,
        'available_languages': ['en', 'hi', 'es', 'fr', 'de', 'ja']
    }
    return render(request, 'faq/dashboard.html', context)