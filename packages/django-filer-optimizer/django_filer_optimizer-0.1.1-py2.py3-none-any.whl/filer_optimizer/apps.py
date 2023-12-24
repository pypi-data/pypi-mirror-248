# coding: utf-8
from django.apps import AppConfig


class FilerOptimizerConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "filer_optimizer"
    verbose_name = "Filer Optimizer"

    def ready(self):
        from . import signals
