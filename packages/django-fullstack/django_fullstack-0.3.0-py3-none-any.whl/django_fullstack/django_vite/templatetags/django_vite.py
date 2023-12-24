from typing import Dict
from django import template
from django.utils.safestring import mark_safe
from django_vite.core.asset_loader import DjangoViteAssetLoader, DEFAULT_APP_NAME

register = template.Library()
loader_instance = DjangoViteAssetLoader.instance()

def generate_vite_tag(method_name, *args, **kwargs):
    return getattr(loader_instance, method_name)(*args, **kwargs)

@register.simple_tag
@mark_safe
def vite_hmr_client(app: str = DEFAULT_APP_NAME, **kwargs: Dict[str, str]) -> str:
    return generate_vite_tag('generate_vite_ws_client', app, **kwargs)

@register.simple_tag
@mark_safe
def vite_asset(path: str, app: str = DEFAULT_APP_NAME, **kwargs: Dict[str, str]) -> str:
    assert path is not None
    return generate_vite_tag('generate_vite_asset', path, app, **kwargs)

@register.simple_tag
@mark_safe
def vite_preload_asset(path: str, app: str = DEFAULT_APP_NAME) -> str:
    assert path is not None
    return generate_vite_tag('preload_vite_asset', path, app)

@register.simple_tag
def vite_asset_url(path: str, app: str = DEFAULT_APP_NAME) -> str:
    assert path is not None
    return generate_vite_tag('generate_vite_asset_url', path, app)

@register.simple_tag
@mark_safe
def vite_legacy_polyfills(app: str = DEFAULT_APP_NAME, **kwargs: Dict[str, str]) -> str:
    return generate_vite_tag('generate_vite_legacy_polyfills', app, **kwargs)

@register.simple_tag
@mark_safe
def vite_legacy_asset(path: str, app: str = DEFAULT_APP_NAME, **kwargs: Dict[str, str]) -> str:
    assert path is not None
    return generate_vite_tag('generate_vite_legacy_asset', path, app, **kwargs)

@register.simple_tag
@mark_safe
def vite_react_refresh(app: str = DEFAULT_APP_NAME) -> str:
    return generate_vite_tag('generate_vite_react_refresh_url', app)
