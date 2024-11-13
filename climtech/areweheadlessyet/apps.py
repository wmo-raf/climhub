from django.apps import AppConfig


class AreWeHeadlessYetConfig(AppConfig):
    name = "climtech.areweheadlessyet"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from .signal_handlers import register_signal_handlers

        register_signal_handlers()
