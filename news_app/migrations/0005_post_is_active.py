# Generated by Django 4.2.17 on 2025-02-02 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_category_name_en_us_category_name_ru_post_text_en_us_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
