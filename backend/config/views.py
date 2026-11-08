from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse


def spa_index(request):
    """Devuelve el index.html de Vue para que funcione el history mode."""
    index = Path(settings.FRONTEND_DIST) / 'index.html'
    if not index.exists():
        raise Http404('frontend/dist/index.html no existe. Ejecuta el build del frontend.')
    return HttpResponse(index.read_bytes(), content_type='text/html; charset=utf-8')
