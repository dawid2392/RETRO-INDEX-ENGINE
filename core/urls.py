from django.urls import path
from django.contrib.auth import views as auth_views

from .views import home, ingest_data, resolve_entities, login_view, dashboard_view, logout_view

app_name = 'core'

urlpatterns = [
    path("", home, name="home"),
    path("api/ingest/", ingest_data, name="ingest_data"),
    path("api/resolve/", resolve_entities, name="resolve_entities"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", logout_view, name="logout"),
]