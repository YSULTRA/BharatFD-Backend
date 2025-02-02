from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # Mark these as read-only to prevent client from sending them

    def to_representation(self, instance):
        lang = self.context.get('lang', 'en')  # Default to 'en' if no language is specified

        # Retrieve the translated question and answer based on the requested language
        translated_question = getattr(instance, f'question_{lang}', instance.question)
        translated_answer = getattr(instance, f'answer_{lang}', instance.answer)

        # Modify the representation to include the translated fields
        data = super().to_representation(instance)
        data['question'] = translated_question
        data['answer'] = translated_answer

        # Add 'created_at' and 'updated_at' explicitly to the response
        data['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data['updated_at'] = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        return data
