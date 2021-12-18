from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from music.models import Album, Contact, Musician, Post, Song
from music.views import get_musician_context


def musician_account_view(request, *args, **kwargs):
    user = request.user
    if not (user.is_authenticated and user.musician):
        return redirect("login")
    musician = user.musician
    return render(request, "accounts/account.html", get_musician_context(musician))


class MusicianCreateView(CreateView):
    model = Musician
    template_name = "accounts/form.html"
    fields = [
        "name", "artistic_name", "email", "date_of_birth", "password"
    ]
    success_url = reverse_lazy("login")
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.password = make_password(form.data["password"])
        instance.save()
        return HttpResponseRedirect(self.success_url)


class MusicianUpdateView(UpdateView):
    model = Musician
    template_name = "accounts/edit_profile.html"
    fields = [
        "image", "artistic_name", "music_styles", "description"
    ]
    success_url = reverse_lazy("accounts:account")

    def get(self, request, **kwargs):
        self.object = self.request.user.musician
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user.musician

    def form_valid(self, form):
        musician = self.get_object()
        musician.music_styles.clear()
        musician.music_styles.add(*form.cleaned_data.pop("music_styles"))
        musician.image = form.cleaned_data.pop("image")
        musician.save()
        # Não sei se isso é necessário mas vou deixar por enquanto...
        Musician.objects.filter(pk=musician.pk).update(**form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())


class MusicianItemView(LoginRequiredMixin):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.musician:
            qs = qs.filter(pk=self.request.user.pk)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["musician"] = self.request.user.musician
        return context


# CONTACT =========

class ContactGenericView(MusicianItemView):
    model = Contact
    template_name = "accounts/contact/form.html"
    fields = ["phonenumber", "kind", "whatsapp"]
    success_url = reverse_lazy("accounts:contacts-list")


class ContactManagerView(ContactGenericView):
    def get_object(self, queryset=None):
        return Contact.objects.filter(musician=self.request.user.musician).get(id=self.kwargs["index"])


class ContactListView(MusicianItemView, ListView):
    model = Contact
    template_name = "accounts/contact/base.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts"] = Contact.objects.filter(musician=self.request.user.musician)
        return context


class ContactCreateView(ContactGenericView, CreateView):
    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.musician = self.request.user.musician
        contact.save()
        return HttpResponseRedirect(self.success_url)


class ContactUpdateView(ContactManagerView, UpdateView):
    def form_valid(self, form):
        contact = self.get_object()
        contact.phonenumber = form.cleaned_data.pop("phonenumber")
        contact.kind = form.cleaned_data.pop("kind")
        contact.whatsapp = form.cleaned_data.pop("whatsapp")
        contact.musician = self.request.user.musician
        contact.save()
        return HttpResponseRedirect(self.success_url)


class ContactDeleteView(ContactManagerView, DeleteView):
    def form_valid(self, form):
        contact = self.get_object()
        contact.delete()
        return HttpResponseRedirect(self.success_url)

# END CONTACT =====


# ALBUM ===========

class AlbumGenericView(MusicianItemView):
    model = Album
    template_name = "accounts/album/form.html"
    fields = ["name", "description", "release_year", "cover"]
    success_url = reverse_lazy("accounts:albums-list")


class AlbumManagerView(AlbumGenericView):
    def get_object(self, queryset=None):
        return Album.objects.filter(musician=self.request.user.musician).get(id=self.kwargs["index"])


class AlbumListView(MusicianItemView, ListView):
    model = Album
    template_name = "accounts/album/base.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["albums"] = Album.objects.filter(musician=self.request.user.musician)
        return context


class AlbumCreateView(AlbumGenericView, CreateView):
    def form_valid(self, form):
        album = form.save(commit=False)
        album.name = form.cleaned_data.pop("name")
        album.description = form.cleaned_data.pop("description")
        album.release_year = form.cleaned_data.pop("release_year")
        album.cover = form.cleaned_data.pop("cover")
        album.musician = self.request.user.musician
        album.save()
        return HttpResponseRedirect(self.success_url)


class AlbumUpdateView(AlbumManagerView, UpdateView):
    def form_valid(self, form):
        album = self.get_object()
        album.name = form.cleaned_data.pop("name")
        album.description = form.cleaned_data.pop("description")
        album.release_year = form.cleaned_data.pop("release_year")
        album.cover = form.cleaned_data.pop("cover")
        album.musician = self.request.user.musician
        album.save()
        return HttpResponseRedirect(self.success_url)


class AlbumDeleteView(AlbumManagerView, DeleteView):
    def form_valid(self, form):
        album = self.get_object()
        album.delete()
        return HttpResponseRedirect(self.success_url)

# END ALBUM =======


# SONG ===========

class SongGenericView(MusicianItemView):
    model = Song
    template_name = "accounts/song/form.html"
    fields = ["name", "order", "file"]
    success_url = reverse_lazy("accounts:albums-list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_id"] = self.kwargs["album_index"]
        return context


class SongManagerView(SongGenericView):
    def get_object(self, queryset=None):
        return Song.objects.get(id=self.kwargs["song_index"], album__musician=self.request.user.musician)


class SongListView(SongGenericView, ListView):
    model = Song
    template_name = "accounts/song/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["songs"] = Song.objects.filter(album__id=self.kwargs["album_index"], album__musician=self.request.user.musician).order_by("order")
        return context


class SongCreateView(SongGenericView, CreateView):
    def form_valid(self, form):
        song = form.save(commit=False)
        song.name = form.cleaned_data.pop("name")
        song.file = form.cleaned_data.pop("file")
        song.album = Album.objects.get(id=self.kwargs["album_index"], musician=self.request.user.musician)
        song.save()
        return HttpResponseRedirect(self.success_url)


class SongUpdateView(SongManagerView, UpdateView):
    def form_valid(self, form):
        song = self.get_object()
        song.name = form.cleaned_data.pop("name")
        song.order = form.cleaned_data.pop("order")
        song.file = form.cleaned_data.pop("file")
        song.save()
        return HttpResponseRedirect(self.success_url)


class SongDeleteView(SongManagerView, DeleteView):
    def form_valid(self, form):
        song = self.get_object()
        song.delete()
        return HttpResponseRedirect(self.success_url)

# END SONG =======


# POST ===========

class PostGenericView(MusicianItemView):
    model = Post
    template_name = "accounts/post/form.html"
    fields = ["title", "text", "image"]
    success_url = reverse_lazy("accounts:posts-list")


class PostManagerView(PostGenericView):
    def get_object(self, queryset=None):
        return Post.objects.filter(musician=self.request.user.musician).get(id=self.kwargs["index"])


class PostListView(MusicianItemView, ListView):
    model = Post
    template_name = "accounts/post/base.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(musician=self.request.user.musician)
        return context


class PostCreateView(PostGenericView, CreateView):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.title = form.cleaned_data.pop("title")
        post.text = form.cleaned_data.pop("text")
        post.image = form.cleaned_data.pop("image")
        post.musician = self.request.user.musician
        post.save()
        return HttpResponseRedirect(self.success_url)


class PostUpdateView(PostManagerView, UpdateView):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.title = form.cleaned_data.pop("title")
        post.text = form.cleaned_data.pop("text")
        post.image = form.cleaned_data.pop("image")
        post.musician = self.request.user.musician
        post.save()
        return HttpResponseRedirect(self.success_url)


class PostDeleteView(PostManagerView, DeleteView):
    def form_valid(self, form):
        post = self.get_object()
        post.delete()
        return HttpResponseRedirect(self.success_url)
