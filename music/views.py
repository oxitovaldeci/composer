from django.shortcuts import render, get_object_or_404, redirect

from .models import Album, Contact, Musician, Song, Post


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
    return render(request, "musician/profile.html", get_musician_context(musician))


def album_view(request, musician_slug=None, album_slug=None, *args, **kwargs):
    if musician_slug == "None":
        if hasattr(request.user, "musician"):
            musician_slug = request.user.musician.slug
        else:
            return redirect("login")

    if album_slug == "None":
        return redirect("music:profile", slug=musician_slug)

    musician = get_object_or_404(Musician, slug=musician_slug)
    album = get_object_or_404(Album, slug=album_slug)
    return render(request, "musician/album.html", {**get_album_context(album), **get_musician_context(musician)})
