# Generated by Django 4.2.1 on 2023-10-07 12:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0036_rename_answer_faq_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("desktop_banner", models.ImageField(upload_to="main_page/")),
                ("mobile_banner", models.ImageField(upload_to="main_page/")),
                ("is_active", models.BooleanField(default=False)),
            ],
        ),
    ]
