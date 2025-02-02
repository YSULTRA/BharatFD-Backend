from celery import shared_task
from googletrans import Translator


translator = Translator()

@shared_task
def translate_faq_task(faq_id, languages):
    from .models import FAQ, FAQTranslation
    try:
        print(f"Starting translation for FAQ ID: {faq_id}")

        # Fetch the FAQ object
        faq = FAQ.objects.get(id=faq_id)
        print(f"Fetched FAQ: {faq}, Question: {faq.question}, Answer: {faq.answer}")

        # Check if the FAQ exists and if question/answer are non-empty
        if not faq.question or not faq.answer:
            print("FAQ is missing a question or answer.")
            return

        # Loop through each language and translate
        for lang in languages:
            print(f"Translating FAQ to language: {lang}")

            # Ensure the fields are strings
            print(f"Type of question: {type(faq.question)}, Type of answer: {type(faq.answer)}")

            if isinstance(faq.question, str) and isinstance(faq.answer, str):
                try:
                    print(f"Translating question: {faq.question} to {lang}")
                    translated_question = translator.translate(faq.question, dest=lang).text
                    print(f"Translated question: {translated_question}")

                    print(f"Translating answer: {faq.answer} to {lang}")
                    translated_answer = translator.translate(faq.answer, dest=lang).text
                    print(f"Translated answer: {translated_answer}")

                    # Store translation in the FAQTranslation model
                    FAQTranslation.objects.create(
                        faq=faq,
                        language_code=lang,
                        translated_question=translated_question,
                        translated_answer=translated_answer
                    )
                    print(f"Translation stored for language: {lang}")

                except Exception as translation_error:
                    print(f"Error translating FAQ for language {lang}: {translation_error}")
            else:
                print(f"Invalid data types for FAQ ID {faq_id}: question={type(faq.question)}, answer={type(faq.answer)}")

    except FAQ.DoesNotExist:
        print(f"FAQ with ID {faq_id} not found.")
    except Exception as e:
        print(f"Error translating FAQ in background: {e}")


@shared_task
def update_faq_translation_task(faq_id, languages):
    from .models import FAQ, FAQTranslation
    try:
        print(f"Starting translation update for FAQ ID: {faq_id}")

        # Fetch the FAQ object
        faq = FAQ.objects.get(id=faq_id)
        print(f"Fetched FAQ: {faq}, Question: {faq.question}, Answer: {faq.answer}")

        # Check if the FAQ exists and if question/answer are non-empty
        if not faq.question or not faq.answer:
            print("FAQ is missing a question or answer.")
            return

        # Loop through each language and update translation if it exists
        for lang in languages:
            print(f"Updating translation for FAQ in language: {lang}")

            if isinstance(faq.question, str) and isinstance(faq.answer, str):
                try:
                    # Check if a translation already exists for this language
                    existing_translation = FAQTranslation.objects.filter(faq=faq, language_code=lang).first()
                    if existing_translation:
                        print(f"Updating existing translation for language: {lang}")
                        translated_question = translator.translate(faq.question, dest=lang).text
                        translated_answer = translator.translate(faq.answer, dest=lang).text

                        # Update existing translation record
                        existing_translation.translated_question = translated_question
                        existing_translation.translated_answer = translated_answer
                        existing_translation.save()

                        print(f"Updated translation for language: {lang}")
                    else:
                        print(f"No existing translation found for language: {lang}")

                except Exception as translation_error:
                    print(f"Error updating FAQ translation for language {lang}: {translation_error}")
            else:
                print(f"Invalid data types for FAQ ID {faq_id}: question={type(faq.question)}, answer={type(faq.answer)}")

    except FAQ.DoesNotExist:
        print(f"FAQ with ID {faq_id} not found.")
    except Exception as e:
        print(f"Error updating FAQ translation in background: {e}")
