import pytest
from django.urls import reverse
from django.test import TestCase
from .models import FAQ, FAQTranslation
from unittest.mock import patch
import os
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'faq_project.settings'


class FAQModelTest(TestCase):

    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Python?",
            answer="Python is a high-level programming language."
        )

    def test_faq_str_method(self):
        self.assertEqual(str(self.faq), "What is Python?")

    def test_faq_answer_field(self):
        self.assertEqual(self.faq.answer, "Python is a high-level programming language.")

    def test_faq_translation_creation(self):
        translation = FAQTranslation.objects.create(
            faq=self.faq,
            language_code="es",
            translated_question="¿Qué es Python?",
            translated_answer="Python es un lenguaje de programación de alto nivel."
        )

        self.assertEqual(str(translation), "es translation of What is Python?")
        self.assertEqual(translation.language_code, "es")
        self.assertEqual(translation.translated_question, "¿Qué es Python?")
        self.assertEqual(translation.translated_answer, "Python es un lenguaje de programación de alto nivel.")

    @patch('googletrans.Translator.translate')
    def test_translate_faq(self, mock_translate):
        mock_translate.return_value.text = "Python es un lenguaje de programación de alto nivel."

        faq = FAQ.objects.create(
            question="What is Python?",
            answer="Python is a high-level programming language."
        )

        translated_faq = FAQTranslation.objects.create(
            faq=faq,
            language_code="es",
            translated_question=mock_translate.return_value.text,
            translated_answer=mock_translate.return_value.text
        )

        self.assertEqual(translated_faq.translated_question, "Python es un lenguaje de programación de alto nivel.")
        self.assertEqual(translated_faq.translated_answer, "Python es un lenguaje de programación de alto nivel.")


class FAQApiTest(TestCase):

    faq_data = {
        "question": "What is Python?",
        "answer": "Python is a high-level programming language."
    }

    def test_create_faq_api(self):
        url = reverse('faq-create')
        response = self.client.post(url, self.faq_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
