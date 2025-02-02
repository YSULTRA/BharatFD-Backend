import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from googletrans import Translator
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from .tasks import translate_faq_task
# Assuming you have added Google Translate API credentials for the translator
translator = Translator()

class FAQ(models.Model):
    question = models.TextField(verbose_name="Question")
    answer = CKEditor5Field('Answer', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class FAQTranslation(models.Model):
    faq = models.ForeignKey(FAQ, related_name="translations", on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    translated_question = models.TextField()
    translated_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.language_code} translation of {self.faq}"

# List of supported languages, you can modify this as needed
SUPPORTED_LANGUAGES =['sq', 'ro', 'hr', 'ne', 'fa', 'cs', 'gu', 'xh', 'ky', 'mi', 'th', 'mr', 'te', 'lo', 'sm', 'is', 'mn', 'sn', 'el', 'sk', 'pt', 'sr', 'haw', 'ml', 'ru', 'hi', 'sv', 'zu', 'ar', 'fy', 'ht', 'ko', 'he', 'si', 'vi', 'ja', 'bn', 'hy', 'ms', 'pl', 'tr', 'my', 'lv', 'bg', 'nl', 'az', 'fr', 'tl', 'en', 'la', 'hu', 'ur', 'id', 'et', 'kn', 'pa', 'ta', 'yi', 'lt', 'es', 'sw', 'it', 'be', 'mk', 'bs', 'or', 'ps', 'so', 'km', 'ka', 'af', 'de', 'eu', 'cy', 'am', 'uk', 'da', 'sd']


  # Example: Spanish, French, German, Hindi, Chinese

# # Translate text into different languages and save translations
# def translate_faq(faq, languages=SUPPORTED_LANGUAGES):
#     for lang in languages:
#         try:
#             translated_question = translator.translate(faq.question, dest=lang).text
#             translated_answer = translator.translate(faq.answer, dest=lang).text

#             # Store translation in the FAQTranslation model
#             FAQTranslation.objects.create(
#                 faq=faq,
#                 language_code=lang,
#                 translated_question=translated_question,
#                 translated_answer=translated_answer
#             )
#         except Exception as e:
#             print(f"Error translating FAQ to {lang}: {e}")

# Automatically translate FAQ after it is saved
# @receiver(post_save, sender=FAQ)
# def create_faq_translations(sender, instance, created, **kwargs):
#     if created:
#         print(f"FAQ created: {instance}")
#         # translate_faq(instance)
#         translate_faq_task.delay(instance.id, SUPPORTED_LANGUAGES)


