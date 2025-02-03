# Create your tests here.  FAQ unit tests
import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import FAQ

class FAQModelTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework."
        )

    def test_translation_fallback(self):
        """Test that English is returned when translation fails"""
        question_hi = self.faq.get_question('hi')
        self.assertEqual(question_hi, self.faq.question)

    def test_cache_mechanism(self):
        """Test that translations are properly cached"""
        # First call should cache the translation
        question_es = self.faq.get_question('es')
        # Second call should use cached version
        cached_question = self.faq.get_question('es')
        self.assertEqual(question_es, cached_question)

class FAQAPITests(APITestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework."
        )

    def test_list_faqs(self):
        """Test retrieving FAQ list"""
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_language_parameter(self):
        """Test language parameter in API"""
        response = self.client.get('/api/faqs/?lang=es')
        self.assertEqual(response.status_code, 200)
