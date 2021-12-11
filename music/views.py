from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404, redirect

from .models import Album, Contact, Musician, Song, Post

from random import choice


def get_musician_context(musician):
    context = {
        "musician": musician,
        "albums": Album.objects.filter(musician=musician),
        "contacts": Contact.objects.filter(musician=musician),
        "posts": Post.objects.filter(musician=musician)
    }
    return context


def get_album_context(album):
    context = {
        "album": album,
        "songs": Song.objects.filter(album=album),
    }
    return context


def profile_view(request, slug=None, *args, **kwargs):
    if slug == "None":
        if hasattr(request.user, "musician"):
            slug = request.user.musician.slug
        else:
            return redirect("login")

    musician = get_object_or_404(Musician, slug=slug)

    context = {**get_musician_context(musician),
            "primary_color": choice(["#cc0000", "#4e9a06", "#edd400", "#3465a4", "#92659a", "#07c7ca"])}

    if request.user.musician == musician:
        form_data = {}
        if request.method == 'POST':
            album_create_form = AlbumCreateForm(request.POST)
            if album_create_form.is_valid():
                album = album_create_form.save(commit=False)
                album.name = album_create_form.cleaned_data.pop("name")
                album.description = album_create_form.cleaned_data.pop("description")
                album.release_year = album_create_form.cleaned_data.pop("release_year")
                album.cover = album_create_form.cleaned_data.pop("cover")
                print("ALBUM COVER = ", album.cover)
                album.musician = musician
                album.save()
                redirect("music:profile", slug="None")
            else:
                pass
        else:
            album_create_form = AlbumCreateForm()
        form_data = {'album_create_form' : album_create_form}
        context.update({**form_data})

    return render(request, "musician/profile.html", context)


def album_view(request, musician_slug=None, album_slug=None, *args, **kwargs):
    if musician_slug == "None":
        if hasattr(request.user, "musician"):
            musician_slug = request.user.musician.slug
        else:
            return redirect("login")

    if album_slug == "None":
        return redirect("music:profile", slug=musician_slug)

    musician = get_object_or_404(Musician, slug=musician_slug)
    album = get_object_or_404(Album, musician=musician, slug=album_slug)
    return render(request, "musician/album.html", {**get_album_context(album), **get_musician_context(musician)})


class AlbumCreateForm(ModelForm):
    class Meta:
        model = Album
        fields = ["name", "description", "release_year", "cover"]