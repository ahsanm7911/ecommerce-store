# Generated by Django 4.2.1 on 2023-07-31 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_confirmedorder_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.BooleanField(default=True),
        ),
    ]
