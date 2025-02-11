# Generated by Django 5.0.9 on 2025-01-30 20:11

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_remove_mapsnippet_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mapsnippet",
            name="body",
            field=wagtail.fields.StreamField(
                [("map_block", 8)],
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"help_text": "Title for the map", "max_length": 255},
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "blank": True,
                            "help_text": "Subheading (optional)",
                            "max_length": 255,
                            "null": True,
                        },
                    ),
                    2: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "features": ["bold", "italic"],
                            "help_text": "Description of the map",
                        },
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Category Name", "max_length": 255, "required": True},
                    ),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"help_text": "Hex code for category color", "required": True},
                    ),
                    5: (
                        "climtech.core.blocks.MultiChoiceBlock",
                        (),
                        {
                            "choices": [
                                ("DZ", "Algeria"),
                                ("AO", "Angola"),
                                ("BJ", "Benin"),
                                ("BW", "Botswana"),
                                ("BF", "Burkina Faso"),
                                ("BI", "Burundi"),
                                ("CM", "Cameroon"),
                                ("CV", "Cape Verde"),
                                ("CF", "Central African Republic"),
                                ("TD", "Chad"),
                                ("KM", "Comoros"),
                                ("CG", "Congo - Brazzaville"),
                                ("CD", "Congo - Kinshasa"),
                                ("CI", "Côte d'Ivoire"),
                                ("DJ", "Djibouti"),
                                ("EG", "Egypt"),
                                ("GQ", "Equatorial Guinea"),
                                ("ER", "Eritrea"),
                                ("SZ", "Eswatini"),
                                ("ET", "Ethiopia"),
                                ("GA", "Gabon"),
                                ("GM", "Gambia"),
                                ("GH", "Ghana"),
                                ("GN", "Guinea"),
                                ("GW", "Guinea-Bissau"),
                                ("KE", "Kenya"),
                                ("LS", "Lesotho"),
                                ("LR", "Liberia"),
                                ("LY", "Libya"),
                                ("MG", "Madagascar"),
                                ("MW", "Malawi"),
                                ("ML", "Mali"),
                                ("MR", "Mauritania"),
                                ("MU", "Mauritius"),
                                ("MA", "Morocco"),
                                ("MZ", "Mozambique"),
                                ("NA", "Namibia"),
                                ("NE", "Niger"),
                                ("NG", "Nigeria"),
                                ("RW", "Rwanda"),
                                ("ST", "São Tomé and Príncipe"),
                                ("SN", "Senegal"),
                                ("SC", "Seychelles"),
                                ("SL", "Sierra Leone"),
                                ("SO", "Somalia"),
                                ("ZA", "South Africa"),
                                ("SS", "South Sudan"),
                                ("SD", "Sudan"),
                                ("TZ", "Tanzania"),
                                ("TG", "Togo"),
                                ("TN", "Tunisia"),
                                ("UG", "Uganda"),
                                ("ZM", "Zambia"),
                                ("ZW", "Zimbabwe"),
                            ]
                        },
                    ),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [[("category_name", 3), ("color", 4), ("countries", 5)]],
                        {},
                    ),
                    7: ("wagtail.blocks.ListBlock", (6,), {"min_num": 1}),
                    8: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("heading", 0),
                                ("subheading", 1),
                                ("description", 2),
                                ("map_categories", 7),
                            ]
                        ],
                        {},
                    ),
                },
                null=True,
            ),
        ),
    ]
