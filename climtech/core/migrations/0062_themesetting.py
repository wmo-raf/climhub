# Generated by Django 5.0.9 on 2024-11-11 12:21

import django.db.models.deletion
import wagtail_color_panel.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0061_remove_homepage_code_snippet"),
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="ThemeSetting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "accent_color",
                    wagtail_color_panel.fields.ColorField(
                        blank=True,
                        default="#007d7e",
                        help_text="Accent color (use color picker). Accent colors are often bright or contrasting to stand out",
                        max_length=7,
                        null=True,
                    ),
                ),
                (
                    "accent_color_dark",
                    wagtail_color_panel.fields.ColorField(
                        blank=True,
                        default="#065354",
                        help_text="Darker Accent color (use color picker). Darker shade of the Accent colors are often bright or contrasting to stand out",
                        max_length=7,
                        null=True,
                    ),
                ),
                (
                    "footer_color_bg",
                    wagtail_color_panel.fields.ColorField(
                        blank=True,
                        default="#065354",
                        help_text="Footer Background color (use color picker)",
                        max_length=7,
                        null=True,
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
