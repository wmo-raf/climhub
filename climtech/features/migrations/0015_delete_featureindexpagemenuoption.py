# Generated by Django 3.2.16 on 2022-10-14 16:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("features", "0014_remove_featuredescription_airtable_record_id"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FeatureIndexPageMenuOption",
        ),
    ]
