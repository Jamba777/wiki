from django.apps import AppConfig


class WikiConfig(AppConfig):
    name = 'api.wiki'

    def ready(self):
        import api.wiki.signals