# Generated by Django 4.2.1 on 2023-09-01 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_confirmedorder_tracking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmedorder',
            name='tracking_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
