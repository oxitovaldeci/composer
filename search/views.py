from django.shortcuts import render
from django.db.models import Q

from music.models import Musician
from music.views import get_musician_context


def search_view(request, *args, **kwargs):
    if hasattr(request.user, "musician"):
        musician = request.user.musician
    else:
        musician = None

    result = Musician.objects.all().order_by('?')[:40]
    query = None
    if request.GET.get("query"):
        query = request.GET.get("query")
        if query == "*":
            result = Musician.objects.all()
        else:
            f = Musician.objects.filter
            result = f(Q(name__unaccent__icontains=query) | Q(artistic_name__unaccent__icontains=query))

    return render(request, "search/search.html", {"result": result, "display_query": query or "Composer", **get_musician_context(musician)})
