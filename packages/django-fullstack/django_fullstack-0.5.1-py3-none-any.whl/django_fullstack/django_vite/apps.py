from django.apps import AppConfig
from django.core import checks
from django_fullstack.django_vite.core.asset_loader import DjangoViteAssetLoader

class DjangoViteAppConfig(AppConfig):
    name = "django_vite for render"
    verbose_name = "Django Vite for render in inertiajs"

    def ready(self) -> None:
        
        DjangoViteAssetLoader.instance()

        checks.register(check_loader_instance, checks.Tags.staticfiles)

def check_loader_instance(**kwargs):
    return DjangoViteAssetLoader.instance().check(**kwargs)
