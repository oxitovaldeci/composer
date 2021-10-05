from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from music.models import Album, Contact, Musician, Song
from music.views import get_musician_context, get_album_context
from composer_utils import cprint


def search_view(request, *args, **kwargs):
    if hasattr(request.user, "musician"):
        musician = request.user.musician
    else:
        musician = None

    result = None
    if request.GET.get("query"):
        query = request.GET.get("query")
        if query == "*":
            result = Musician.objects.all()
        else:
            result = Musician.objects.filter(name__unaccent__icontains=query)

    return render(request, "search/search.html", {"result": result, **get_musician_context(musician)})
