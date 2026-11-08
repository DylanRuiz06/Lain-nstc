from django.urls import path

from . import views

urlpatterns = [
    path('csrf/', views.csrf_view, name='csrf'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.me_view, name='me'),
    path('regions/', views.regions_collection, name='regions-collection'),
    path('regions/<int:pk>/', views.region_detail, name='region-detail'),
    path('regions/<int:pk>/biotopes/', views.region_biotopes, name='region-biotopes'),
    path('biotopes/', views.biotopes_collection, name='biotopes-collection'),
    path('biotopes/<int:pk>/', views.biotope_detail, name='biotope-detail'),
    path('species/', views.species_collection, name='species-collection'),
    path('species/<int:pk>/', views.species_detail, name='species-detail'),
]
