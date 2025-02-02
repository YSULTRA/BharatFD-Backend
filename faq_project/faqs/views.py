from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import FAQ, FAQTranslation
from .serializers import FAQSerializer
from django.core.cache import cache
from django.shortcuts import render
import requests
from .signals import LANGUAGE_NAMES
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from django.http import request


class FAQListView(APIView):
    def get(self, request):
        # Get the language from the query parameter, default to 'en' if not provided
        lang = request.query_params.get('lang', 'en')

        faq_data = []
        faqs = FAQ.objects.all().only('id', 'question', 'answer', 'created_at', 'updated_at')

        for faq in faqs:
            # Generate the cache key using the object ID and language
            cache_key = f"faq_{faq.id}_{lang}"

            # Check if the FAQ data is already cached
            cached_faq = cache.get(cache_key)

            if cached_faq:
                # If cached data exists, use it
                faq_data.append(cached_faq)
            else:
                # If no cached data exists, check if translation exists for the current language
                faq_translation = None
                if lang != 'en':
                    faq_translation = FAQTranslation.objects.filter(faq=faq, language_code=lang).first()

                # Use translation if available, otherwise fallback to English
                if faq_translation:
                    cached_faq = {
                        'id': faq.id,
                        'question': faq_translation.translated_question,
                        'answer': faq_translation.translated_answer,
                        'created_at': faq.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'updated_at': faq.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                else:
                    cached_faq = {
                        'id': faq.id,
                        'question': faq.question,
                        'answer': faq.answer,
                        'created_at': faq.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'updated_at': faq.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }

                # Save the FAQ data in the cache for future requests
                cache.set(cache_key, cached_faq, timeout=30)  # Cache timeout of 24 hours
                faq_data.append(cached_faq)

        # Return the FAQ data (translated or original)
        return Response(faq_data, status=status.HTTP_200_OK)

class FAQCreateView(APIView):
    def post(self, request):
        print("User making request:", request.user)
        print("Request headers:", request.headers)
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            faq = serializer.save()

            # Invalidate the cache for all languages (English and others)
            with transaction.atomic():
                # Delete all language-specific cache entries
                cache.delete(f"faq_{faq.id}_en")  # Delete English cache
                faq_translations = FAQTranslation.objects.filter(faq=faq)
                for translation in faq_translations:
                    cache.delete(f"faq_{faq.id}_{translation.language_code}")  # Delete each translation cache

                # Set the new cache for English (fallback)
                cache.set(f"faq_{faq.id}_en", {
                    'id': faq.id,
                    'question': faq.question,
                    'answer': faq.answer,
                    'created_at': faq.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_at': faq.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }, timeout=30)  # Cache timeout of 24 hours

                # Update the cache for translations (if any)
                for translation in faq_translations:
                    cache.set(f"faq_{faq.id}_{translation.language_code}", {
                        'id': faq.id,
                        'question': translation.translated_question,
                        'answer': translation.translated_answer,
                        'created_at': faq.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'updated_at': faq.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    }, timeout=30)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class FAQUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, pk):
        print("User making request:", request.user)
        print("Request headers:", request.headers)
        try:
            faq = FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            return Response({"detail": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FAQSerializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            updated_faq = serializer.save()

            # Invalidate the cache for all languages (English and others)
            with transaction.atomic():
                # Delete all language-specific cache entries
                cache.delete(f"faq_{updated_faq.id}_en")  # Delete English cache
                faq_translations = FAQTranslation.objects.filter(faq=updated_faq)
                for translation in faq_translations:
                    cache.delete(f"faq_{updated_faq.id}_{translation.language_code}")  # Delete each translation cache

                # Set the updated cache for English (fallback)
                cache.set(f"faq_{updated_faq.id}_en", {
                    'id': updated_faq.id,
                    'question': updated_faq.question,
                    'answer': updated_faq.answer
                }, timeout=30)  # Cache timeout of 24 hours

                # Update the cache for translations (if any)
                for translation in faq_translations:
                    cache.set(f"faq_{updated_faq.id}_{translation.language_code}", {
                        'id': updated_faq.id,
                        'question': translation.translated_question,
                        'answer': translation.translated_answer
                    }, timeout=30)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def homepage(request):
    context = {
        'message': 'Hello, Django!',
        'languages': LANGUAGE_NAMES
    }
    return render(request,'homepage.html',context)

def create_faq(request):
    return render(request, 'createFAQ.html')