from .models import SiteSettings


def site_settings(request):
    """Make site settings available to all templates"""
    return {"site_settings": SiteSettings.get_settings()}
