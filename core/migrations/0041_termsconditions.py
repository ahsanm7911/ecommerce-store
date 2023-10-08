# Generated by Django 4.2.1 on 2023-10-08 07:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "core",
            "0040_rename_secondary_banner_homepage_secondary_desktop_banner_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="TermsConditions",
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
                ("description", models.TextField()),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title_tag", models.CharField(max_length=255)),
                ("meta_description", models.TextField()),
            ],
        ),
    ]
