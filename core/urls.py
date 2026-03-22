from django.urls import path

from .views import home, ingest_data, resolve_entities

app_name = 'core'

urlpatterns = [
    path("", home, name="home"),
    path("api/ingest/", ingest_data, name="ingest_data"),
    path("api/resolve/", resolve_entities, name="resolve_entities"),
]