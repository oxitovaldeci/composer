from django.urls import path

from . import views as acc_views

app_name = "accounts"
urlpatterns = [
    path("update/", acc_views.MusicianUpdateView.as_view(), name="update"),
    path("create/", acc_views.MusicianCreateView.as_view(), name="create"),
    path("", acc_views.musician_account_view, name="account"),

    path("contacts/", acc_views.ContactListView.as_view(), name="contacts-list"),
    path("contacts/add/", acc_views.ContactCreateView.as_view(), name="contacts-create"),
    path("contacts/update/<int:index>", acc_views.ContactUpdateView.as_view(), name="contacts-update"),
    path("contacts/delete/<int:index>", acc_views.ContactDeleteView.as_view(), name="contacts-delete"),

    path("albums/", acc_views.AlbumListView.as_view(), name="albums-list"),
    path("albums/add/", acc_views.AlbumCreateView.as_view(), name="albums-create"),
    path("albums/update/<int:index>", acc_views.AlbumUpdateView.as_view(), name="albums-update"),
    path("albums/delete/<int:index>", acc_views.AlbumDeleteView.as_view(), name="albums-delete"),

    path("albums/<int:album_index>/songs/", acc_views.SongListView.as_view(), name="songs-list"),
    path("albums/<int:album_index>/songs/add/", acc_views.SongCreateView.as_view(), name="songs-create"),
    path("albums/<int:album_index>/songs/update/<int:song_index>", acc_views.SongUpdateView.as_view(), name="songs-update"),
    path("albums/<int:album_index>/songs/delete/<int:song_index>", acc_views.SongDeleteView.as_view(), name="songs-delete"),
]
