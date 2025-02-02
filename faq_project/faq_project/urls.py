from django.urls import path ,include
from django.contrib import admin
from django.http import HttpResponse
from faqs.views import FAQListView ,FAQCreateView,FAQUpdateView, create_faq# Assuming your FAQ List view is defined here
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from faqs.views import homepage



urlpatterns = [
    path('', homepage, name='homepage'),  # Root URL view
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('api/faqs/', FAQListView.as_view(), name='faq-list'),
    # View to create a new FAQ (POST)
    path('api/faqs/create/', FAQCreateView.as_view(), name='faq-create'),

    # View to update an existing FAQ (PUT)
    path('api/faqs/<int:pk>/update/', FAQUpdateView.as_view(), name='faq-update'),
    path('create/',create_faq , name='faq-create'),
]

# Add media URL handling (only in development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
