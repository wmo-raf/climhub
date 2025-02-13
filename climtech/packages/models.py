from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Prefetch
from django.db.models.functions import Lower
from django.urls import reverse
import uuid

from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from climtech.utils.models import CrossPageMixin, SocialMediaMixin

warning = """
    <p>
        Edit this data on Djangopackages.org.<br>
        `Settings > Django Packages > Import` will override this data.
    </p>
"""

readonly = forms.TextInput(attrs={"readonly": True})

default_about_text = " ".join(
    """
    <p>
        Projects listed on ClimHub are <i>third-party</i> packages.<br/>
        They are not vetted nor endorsed by ClimHub.<br/>
        Use them at your own risk.</p>
        <p>This page collects girds and packages from djangopackages.org.<br/>
    </p>
""".split()
)  # Split/join to normalise whitespace


class PackagesPage(Page, SocialMediaMixin, CrossPageMixin):
    max_count = 1
    parent_page_types = ["core.HomePage"]
    subpage_types = []

    subtitle = models.CharField(max_length=255)
    about_title = models.CharField(max_length=255, default="About")
    about_text = RichTextField(
         features=["bold", "italic", "link"]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        packages = Package.objects.filter(publish=True).order_by(Lower("title"))
        context.update(
            {
                "grids": Grid.objects.filter(publish=True)
                .order_by(Lower("title"))
                .prefetch_related(Prefetch("packages", queryset=packages))
            }
        )
        return context

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("about_title"),
        FieldPanel("about_text"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("about_title"),
        index.SearchField("about_text"),
    ]

class Package(models.Model):
    publish = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    uid = models.AutoField(primary_key=True, unique=True, editable=False)

    repo_url = models.URLField(blank=True)
    repo_description = models.TextField(blank=True)
    pypi_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)

    panels = [
        FieldPanel("publish"),
        MultiFieldPanel(
            [
                HelpPanel(content=warning),
                FieldPanel("title",),
                FieldPanel("slug",),
                FieldPanel("repo_description"),
                FieldPanel("repo_url"),
            ],
            heading="DjangoPackages.org data",
        ),
    ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.pypi_url

    def get_admin_url(self):
        if hasattr(self, "model_viewset"):
            return reverse(self.model_viewset.get_url_name("edit"), args=(self.id,))

    def links(self):
        links = []
        if self.repo_url:
            links.append((self.repo_url, "Repo"))
        if self.pypi_url:
            links.append((self.pypi_url, "PyPi"))
        if self.documentation_url:
            links.append((self.documentation_url, "Docs"))
        return links


class Grid(models.Model):
    publish = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    packages = models.ManyToManyField(Package, blank=True)

    panels = [
        FieldPanel("publish"),
        MultiFieldPanel(
            [
                HelpPanel(content=warning),
                FieldPanel("title"),
                FieldPanel("slug"),
                FieldPanel("description"),
                FieldPanel("packages"),
            ],
            heading="Data",
        ),
    ]

    def __str__(self):
        return self.title

    def get_admin_url(self):
        if hasattr(self, "model_viewset"):
            return reverse(self.model_viewset.get_url_name("edit"), args=(self.id,))

    def display_title(self):
        return (
            self.title[8:].title() if self.title.startswith("ClimHub ") else self.title
        )
