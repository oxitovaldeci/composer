from django.views.generic.base import TemplateView

from music.models import Album, Song


class IndexTemplateView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        songs = Song.objects.all()
        user = self.request.user
        user_is_musician = hasattr(user, "musician")
        albums = Album.objects.all()
        # albums_count = albums.count()

        if user_is_musician:
            context["musician"] = user.musician

        if songs:
            context["song"] = songs.order_by("?")[0]

        if albums:
            context["album"] = albums.order_by("?")[0]

            context["lastAlbums"] = albums.order_by("?")[:5]

        return context
