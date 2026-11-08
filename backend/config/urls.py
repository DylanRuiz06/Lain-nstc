from django.urls import include, path, re_path

from .views import spa_index

urlpatterns = [
    path('api/', include('catalog.urls')),
    re_path(r'^(?!api/|static/).*$', spa_index, name='spa'),
]
