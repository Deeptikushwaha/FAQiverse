from django.db import models

# Create your models here.    #faq models and translation logic
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator
import json

class FAQ(models.Model):
    #Base fields
    question = models.TextField(help_text="Enter the question in English")
    answer = RichTextField(help_text="Enter the answer in English")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #dynamic translations field
    translations = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:100]

    def get_translation(self, field, lang):
        print(f"Translating {field} to {lang}")
        """Get translated text for a given field and language."""
        if lang == 'en':
            return getattr(self, field)
            
        cache_key = f'faq_{self.id}_{field}_{lang}'
        # Try to get from cache first
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # If not in cache, check translations field
        if self.translations.get(lang,{}).get(field):
            translation = self.translations[lang][field]
            cache.set(cache_key, translation, timeout=86400)#Cache for 24 hours
            return translation
        # If no translation exists, translate using Google Translate
        translator = Translator()
        text = getattr(self, field)
        try:
            translation = translator.translate(text, dest=lang).text
            # Update translations field
            current_translations = self.translations.copy()
            if lang not in current_translations:
                current_translations[lang] = {}
            current_translations[lang][field] = translation
            self.translations = current_translations
            self.save(update_fields=['translations'])
            #cache the result
            cache.set(cache_key, translation, timeout=86400)
            return translation
        except:
            # Fallback to English if translation fails
            return getattr(self, field)
    
    def get_question(self, lang='en'):
        """Get translated question."""
        if lang == 'en':
            return self.question
        return self.get_translation('question', lang)

    def get_answer(self, lang='en'):
        """Get translated answer."""
        if lang == 'en':
            return self.answer
        return self.get_translation('answer', lang)