# Generated by Django 4.2.1 on 2023-09-16 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_category_keywords_category_meta_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='alt_tag',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='alt_tag',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
