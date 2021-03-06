import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.http import HttpResponse

try:
    from django.apps import apps

    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

try:
    model = get_model(settings.HEALTH_MODEL)
except:
    raise ImproperlyConfigured(
        'settings.HEALTH_MODEL doesn\'t resolve to a useable model')

log = logging.getLogger(__name__)


def check_data(request):
    """
    Check health BBGA data
    """
    if model.objects.count() < 1000000:
        log.error("Not enough BBGA data found")
        return HttpResponse(
            "No sufficient BBGA data found",
            content_type="text/plain", status=500)

    return HttpResponse(
        "Data OK", content_type='text/plain', status=200)


def health(request):
    # check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            assert cursor.fetchone()
    except:
        log.exception("Database connectivity failed")
        return HttpResponse(
            "Database connectivity failed",
            content_type="text/plain", status=500)

    # check debug
    if settings.DEBUG:
        log.exception("Debug mode not allowed in production")
        return HttpResponse(
            "Debug mode not allowed in production",
            content_type="text/plain", status=500)

    return HttpResponse(
        "Health OK", content_type='text/plain', status=200)
