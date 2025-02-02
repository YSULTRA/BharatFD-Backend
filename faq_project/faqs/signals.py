from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FAQ
from .models import FAQTranslation
from googletrans import Translator
from .tasks import translate_faq_task ,update_faq_translation_task

translator = Translator()

SUPPORTED_LANGUAGES =['sq', 'ro', 'hr', 'ne', 'fa','hi','cs', 'gu', 'xh', 'ky', 'mi', 'th', 'mr', 'te', 'lo', 'sm', 'is', 'mn', 'sn', 'el', 'sk', 'pt', 'sr', 'haw', 'ml', 'ru', 'hi', 'sv', 'zu', 'ar', 'fy', 'ht', 'ko', 'he', 'si', 'vi', 'ja', 'bn', 'hy', 'ms', 'pl', 'tr', 'my', 'lv', 'bg', 'nl', 'az', 'fr', 'tl', 'en', 'la', 'hu', 'ur', 'id', 'et', 'kn', 'pa', 'ta', 'yi', 'lt', 'es', 'sw', 'it', 'be', 'mk', 'bs', 'or', 'ps', 'so', 'km', 'ka', 'af', 'de', 'eu', 'cy', 'am', 'uk', 'da', 'sd']

LANGUAGE_NAMES = {
    'sq': 'Albanian', 'ro': 'Romanian', 'hr': 'Croatian', 'ne': 'Nepali', 'fa': 'Persian', 'hi': 'Hindi',
    'cs': 'Czech', 'gu': 'Gujarati', 'xh': 'Xhosa', 'ky': 'Kyrgyz', 'mi': 'Māori', 'th': 'Thai', 'mr': 'Marathi',
    'te': 'Telugu', 'lo': 'Lao', 'sm': 'Samoan', 'is': 'Icelandic', 'mn': 'Mongolian', 'sn': 'Shona', 'el': 'Greek',
    'sk': 'Slovak', 'pt': 'Portuguese', 'sr': 'Serbian', 'haw': 'Hawaiian', 'ml': 'Malayalam', 'ru': 'Russian',
    'sv': 'Swedish', 'zu': 'Zulu', 'ar': 'Arabic', 'fy': 'Frisian', 'ht': 'Haitian Creole', 'ko': 'Korean',
    'he': 'Hebrew', 'si': 'Sinhalese', 'vi': 'Vietnamese', 'ja': 'Japanese', 'bn': 'Bengali', 'hy': 'Armenian',
    'ms': 'Malay', 'pl': 'Polish', 'tr': 'Turkish', 'my': 'Burmese', 'lv': 'Latvian', 'bg': 'Bulgarian',
    'nl': 'Dutch', 'az': 'Azerbaijani', 'fr': 'French', 'tl': 'Tagalog', 'en': 'English', 'la': 'Latin',
    'hu': 'Hungarian', 'ur': 'Urdu', 'id': 'Indonesian', 'et': 'Estonian', 'kn': 'Kannada', 'pa': 'Punjabi',
    'ta': 'Tamil', 'yi': 'Yiddish', 'lt': 'Lithuanian', 'es': 'Spanish', 'sw': 'Swahili', 'it': 'Italian',
    'be': 'Belarusian', 'mk': 'Macedonian', 'bs': 'Bosnian', 'or': 'Odia', 'ps': 'Pashto', 'so': 'Somali',
    'km': 'Khmer', 'ka': 'Georgian', 'af': 'Afrikaans', 'de': 'German', 'eu': 'Basque', 'cy': 'Welsh',
    'am': 'Amharic', 'uk': 'Ukrainian', 'da': 'Danish', 'sd': 'Sindhi'
}
@receiver(post_save, sender=FAQ)
def create_faq_translations(sender, instance, created, **kwargs):
    if created:
        print(f"FAQ created: {instance}")
        # translate_faq(instance)
        translate_faq_task.delay(instance.id, SUPPORTED_LANGUAGES)
    else:
        # If the FAQ is updated, update existing translations
        print(f"FAQ updated: {instance}")
        existing_translations = FAQTranslation.objects.filter(faq=instance)

        if existing_translations.exists():
            # If translations already exist, update them
            languages_to_update = [translation.language_code for translation in existing_translations]
            update_faq_translation_task.delay(instance.id, languages_to_update)
        # else:
        #     # If no translations exist, create new translations
        #     translate_faq_task.delay(instance.id, SUPPORTED_LANGUAGES)