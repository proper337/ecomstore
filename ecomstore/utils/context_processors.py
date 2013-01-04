from ecomstore import settings
from ecomstore.catalog.models import Category

def ecomstore(request):
    """ context processor for the site templates """
    return {
#       'active_categories': Category.objects.filter(is_active=True), 
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
#       'analytics_tracking_id': settings.ANALYTICS_TRACKING_ID,
        'request': request
    }
