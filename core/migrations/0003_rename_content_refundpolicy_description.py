# Generated by Django 4.2.1 on 2023-07-24 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_refundpolicy_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refundpolicy',
            old_name='content',
            new_name='description',
        ),
    ]
