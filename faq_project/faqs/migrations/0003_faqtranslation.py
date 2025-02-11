# Generated by Django 5.0.3 on 2025-02-01 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0002_alter_faq_answer_alter_faq_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(max_length=10)),
                ('translated_question', models.TextField()),
                ('translated_answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('faq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='faqs.faq')),
            ],
        ),
    ]
