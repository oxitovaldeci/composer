from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls"), name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("music/", include("music.urls"), name="music"),
    path("accounts/", include("accounts.urls"), name="accounts"),
    path("search/", include("search.urls"), name="search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
