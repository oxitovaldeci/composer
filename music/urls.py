from django.urls import path

from . import views

app_name = "music"
urlpatterns = [
    path("<slug:slug>", views.profile_view, name="profile"),
    path("<slug:musician_slug>/<slug:album_slug>", views.album_view, name="album"),
]
