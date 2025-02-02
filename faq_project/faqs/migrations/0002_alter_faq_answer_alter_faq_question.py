# Generated by Django 5.0.3 on 2025-02-01 12:55

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.TextField(verbose_name='Question'),
        ),
    ]
