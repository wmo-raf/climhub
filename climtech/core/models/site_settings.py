import logging

from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel

from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtailcache.cache import clear_cache
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

@register_setting
class ThemeSetting(BaseSiteSetting):
    accent_color =  ColorField(blank=True, null=True, default="#09aaff",
                               help_text=_("Accent color (use color picker). Accent colors are often bright or contrasting to stand out"))
    accent_color_dark =  ColorField(blank=True, null=True, default="#065354",
                               help_text=_("Darker Accent color (use color picker). Darker shade of the Accent colors are often bright or contrasting to stand out"))
    footer_color_bg = ColorField(blank=True, null=True, default="#065354",
                               help_text=_("Footer Background color (use color picker)"))


    panels = [
        NativeColorPanel('accent_color'),
        NativeColorPanel('accent_color_dark'),
        NativeColorPanel('footer_color_bg'),
    ]

# clear wagtail cache on saving the following models
@receiver(post_save, sender=ThemeSetting)
def handle_clear_wagtail_cache(sender, **kwargs):
    logging.info("[WAGTAIL_CACHE]: Clearing cache")
    clear_cache()
