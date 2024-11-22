from django.conf import settings
from climtech.core.models.site_settings import ThemeSetting

def theme(request):

    try:

        theme = ThemeSetting.for_request(request)

        return {
            'accent_color':theme.accent_color,
            'accent_color_dark':theme.accent_color_dark,
            'footer_color_bg':theme.footer_color_bg
        }
    except:
        return {
            'accent_color':'#333',
            'accent_color_dark':'#333',
            'footer_color_bg':'#333'
        }

def global_pages(request):
    return {
        "BASE_URL": getattr(settings, "BASE_URL", ""),
        "DEBUG": getattr(settings, "DEBUG", ""),
        "FB_APP_ID": getattr(settings, "FB_APP_ID", ""),
        "GOOGLE_TAG_MANAGER_ID": getattr(settings, "GOOGLE_TAG_MANAGER_ID", ""),
        "MAILCHIMP_ACCOUNT_ID": getattr(settings, "MAILCHIMP_ACCOUNT_ID", ""),
        "MAILCHIMP_NEWSLETTER_ID": getattr(settings, "MAILCHIMP_NEWSLETTER_ID", ""),
    }
