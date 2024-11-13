# Generated by Django 3.2.18 on 2023-05-19 18:37

from django.db import migrations

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks

import climtech.utils.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("standardpage", "0006_streamfield_use_json_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standardpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "h2",
                        wagtail.blocks.CharBlock(
                            form_classname="title",
                            icon="title",
                            template="patterns/components/streamfields/headings/heading-2.html",
                        ),
                    ),
                    (
                        "h3",
                        wagtail.blocks.CharBlock(
                            form_classname="title",
                            icon="title",
                            template="patterns/components/streamfields/headings/heading-3.html",
                        ),
                    ),
                    (
                        "h4",
                        wagtail.blocks.CharBlock(
                            form_classname="title",
                            icon="title",
                            template="patterns/components/streamfields/headings/heading-4.html",
                        ),
                    ),
                    (
                        "paragraph",
                        wagtail.blocks.RichTextBlock(
                            icon="pilcrow",
                            template="patterns/components/streamfields/rich_text_block/rich_text_block.html",
                        ),
                    ),
                    (
                        "blockquote",
                        wagtail.blocks.CharBlock(
                            form_classname="title",
                            icon="openquote",
                            template="patterns/components/streamfields/quotes/standalone_quote_block.html",
                        ),
                    ),
                    (
                        "image",
                        wagtail.images.blocks.ImageChooserBlock(
                            icon="image",
                            template="patterns/components/streamfields/image/image.html",
                        ),
                    ),
                    (
                        "document",
                        wagtail.documents.blocks.DocumentChooserBlock(
                            icon="doc-full-inverse",
                            template="patterns/components/streamfields/document/document.html",
                        ),
                    ),
                    (
                        "embed",
                        wagtail.embeds.blocks.EmbedBlock(
                            icon="code",
                            template="patterns/components/streamfields/embed/embed.html",
                        ),
                    ),
                    (
                        "markdown",
                        climtech.utils.blocks.MarkDownBlock(
                            template="patterns/components/streamfields/code_block/code_block.html"
                        ),
                    ),
                    (
                        "codeblock",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "language",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("bash", "Bash/Shell"),
                                            ("css", "CSS"),
                                            ("django", "Django templating language"),
                                            ("html", "HTML"),
                                            ("javascript", "Javascript"),
                                            ("python", "Python"),
                                            ("scss", "SCSS"),
                                        ]
                                    ),
                                ),
                                ("code", wagtail.blocks.TextBlock()),
                            ],
                            template="patterns/components/streamfields/code_block/code_block.html",
                        ),
                    ),
                    (
                        "teaser",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "page",
                                    wagtail.blocks.PageChooserBlock(
                                        page_type=["blog.BlogPage"], required=False
                                    ),
                                ),
                                (
                                    "url_chooser",
                                    wagtail.blocks.URLBlock(required=False),
                                ),
                                (
                                    "image_for_external_link",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    "heading_for_external_link",
                                    wagtail.blocks.TextBlock(required=False),
                                ),
                                (
                                    "subheading_for_ext_link",
                                    wagtail.blocks.TextBlock(
                                        label="Subheading for external link",
                                        required=False,
                                    ),
                                ),
                            ],
                            group="CTA options",
                        ),
                    ),
                    (
                        "get_started_block",
                        wagtail.snippets.blocks.SnippetChooserBlock(
                            "core.GetStartedSnippet",
                            group="CTA options",
                            icon="th-list",
                            template="patterns/components/streamfields/get_started_block/get_started_block.html",
                        ),
                    ),
                    (
                        "sign_up_form",
                        wagtail.snippets.blocks.SnippetChooserBlock(
                            "core.SignupFormSnippet",
                            group="CTA options",
                            icon="envelope-open-text",
                            template="patterns/components/streamfields/sign_up_form_block/sign_up_form_block.html",
                        ),
                    ),
                    (
                        "highlight",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(max_length=100)),
                                (
                                    "description",
                                    wagtail.blocks.TextBlock(required=False),
                                ),
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "image_on_right",
                                    wagtail.blocks.BooleanBlock(
                                        default=False, required=False
                                    ),
                                ),
                                (
                                    "meta_text",
                                    wagtail.blocks.CharBlock(
                                        max_length=50, required=False
                                    ),
                                ),
                                (
                                    "meta_icon",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("arrow-alt", "Arrow alt"),
                                            ("arrow-in-circle", "Arrow in circle"),
                                            ("arrow-in-square", "Arrow in square"),
                                            ("arrows", "Arrows"),
                                            ("blog", "Blog"),
                                            ("bread", "Bread"),
                                            ("briefcase", "Briefcase"),
                                            ("building", "Building"),
                                            ("calendar", "Calendar"),
                                            ("code-file", "Code File"),
                                            ("document", "Document"),
                                            ("envelope", "Envelope"),
                                            ("explanation", "Explanation"),
                                            ("eye", "Eye"),
                                            ("flame", "Flame"),
                                            ("friends", "Friends"),
                                            ("github", "Github"),
                                            ("handshake", "Handshake"),
                                            ("heart", "Heart"),
                                            ("history", "History"),
                                            ("id-card", "ID Card"),
                                            ("image", "Image"),
                                            ("knife-fork", "Knife Fork"),
                                            ("leaf", "Leaf"),
                                            ("location-pin", "Location Pin"),
                                            ("map", "Map"),
                                            ("magnifying-glass", "Magnifying Glass"),
                                            ("money", "Money"),
                                            ("moon", "Moon"),
                                            ("one-two-steps", "One Two Steps"),
                                            ("padlock", "Padlock"),
                                            ("paper-plane", "Paper Plane"),
                                            ("paper-stack", "Paper Stack"),
                                            ("pen-checkbox", "Pen Checkbox"),
                                            ("person-in-tie", "Person in Tie"),
                                            ("python", "Python"),
                                            (
                                                "question-mark-circle",
                                                "Question Mark Circle",
                                            ),
                                            ("quotes", "Quotes"),
                                            ("release-cycle", "Release Cycle"),
                                            ("roadmap", "Roadmap"),
                                            ("rocket", "Rocket"),
                                            ("rollback", "Rollback"),
                                            ("slack", "Slack"),
                                            ("speech-bubble", "Speech Bubble"),
                                            ("sun-cloud", "Sun Cloud"),
                                            ("table-tennis", "Table Tennis"),
                                            ("tree", "Tree"),
                                            ("wordpress", "Wordpress"),
                                            ("world", "World"),
                                        ],
                                        required=False,
                                    ),
                                ),
                                (
                                    "cta",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "text",
                                                wagtail.blocks.CharBlock(
                                                    label="CTA text",
                                                    max_length=255,
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "cta_page",
                                                wagtail.blocks.PageChooserBlock(
                                                    label="CTA page", required=False
                                                ),
                                            ),
                                            (
                                                "cta_url",
                                                wagtail.blocks.URLBlock(
                                                    label="CTA URL", required=False
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
