from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField(help_text="Enter the question in English")
    answer = RichTextField(help_text="Enter the answer in English")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    translations = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:100]

    def get_translation(self, field, lang):
        if lang == 'en':
            return getattr(self, field)
            
        cache_key = f'faq_{self.id}_{field}_{lang}'
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            translator = Translator()
            text = getattr(self, field)
            translation = translator.translate(text, dest=lang).text
            cache.set(cache_key, translation, timeout=86400)
            return translation
        except:
            return getattr(self, field)
