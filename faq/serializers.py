from rest_framework import serializers
from .models import FAQ
#faq serializers
class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']
    
    def get_question(self, obj):
        lang = self.context['request'].query_params.get('lang', 'en')
        return obj.get_question(lang)

    def get_answer(self, obj):
        lang = self.context['request'].query_params.get('lang', 'en')
        return obj.get_answer(lang)