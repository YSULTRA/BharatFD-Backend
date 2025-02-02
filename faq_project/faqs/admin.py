from django.contrib import admin
from faqs.models import FAQ,FAQTranslation
# Register your models here.


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
  list_display = ('question',
                  'answer',
                  'created_at',
                  'updated_at')

  search_fields =['question']

  sortable_by = ('created_at','updated_at','question','answer')
  ordering = ('-created_at','-updated_at','-question','-answer')



class FAQTranslationAdmin(admin.ModelAdmin):
    list_display = ('faq', 'language_code', 'translated_question', 'created_at', 'updated_at')  # Customize fields for translations
    search_fields = ('faq__question', 'language_code')  # Add search functionality for translations




admin.site.register(FAQTranslation, FAQTranslationAdmin)