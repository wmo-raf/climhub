# Generated by Django 1.9.8 on 2016-12-01 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("features", "0004_featuredescription_featuredescriptionfeatureaspect"),
    ]

    operations = [
        migrations.AddField(
            model_name="featureaspect",
            name="video_url",
            field=models.URLField(blank=True),
        ),
    ]
