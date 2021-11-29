from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User


class MusicStyle(models.Model):
    name = models.CharField(_("Nome"), max_length=150, null=False, blank=False)
    slug = models.SlugField(_("Slug"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Estilo Musical"
        verbose_name_plural = "Estilos Musicais"


class Contact(models.Model):
    KIND_PHONE_CHOICES = (
        ("C", "Celular"),
        ("F", "Fixo"),
    )
    phonenumber = models.CharField(_("Telefone"), max_length=50)
    kind = models.CharField(_("Tipo"), max_length=1, choices=KIND_PHONE_CHOICES)
    whatsapp = models.BooleanField(_("WhatsApp?"), default=True)
    musician = models.ForeignKey("music.Musician", verbose_name=_("Músico"), on_delete=models.CASCADE)

    def __str__(self):
        return self.phonenumber

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"


class SocialMedia(models.Model):
    SOCIAL_MEDIA_CHOICES = (
        ("FB", "Facebook"),
        ("IS", "Instagram"),
        ("TT", "Twitter")
    )

    url = models.URLField(_("URL"), max_length=200)
    kind = models.CharField(_("Tipo"), max_length=50, choices=SOCIAL_MEDIA_CHOICES)
    musician = models.ForeignKey("music.Musician", verbose_name=_("Músico"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.musician.name} - {self.kind} - {self.url}"

    class Meta:
        verbose_name = "Mídia Social"
        verbose_name_plural = "Mídias Sociais"


class Musician(User):
    name = models.CharField("Nome", max_length=100)
    artistic_name = models.CharField("Nome Artístico", max_length=100)
    date_of_birth = models.DateField("Data de Nascimento", blank=False, null=True)
    description = models.TextField(_("Descrição do Perfil"), blank=True, null=True)
    image = models.ImageField(_("Foto"), upload_to="images/profile/", default='profile_placeholder.png')
    slug = models.SlugField(_("Slug"), null=True)

    music_styles = models.ManyToManyField("music.MusicStyle", verbose_name=_("Estilo Musical"), blank=True)

    created_at = models.DateTimeField(_("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Data de Última Modificação"), auto_now=True)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Musician._meta.fields]

    def __str__(self):
        return self.name

    @property
    def styles(self):
        response = []
        for style in self.music_styles.all():
            response.append(style.name)
        return ", ".join(response)

    class Meta:
        verbose_name = "Músico"
        verbose_name_plural = "Músicos"


class Album(models.Model):
    name = models.CharField(_("Nome"), max_length=50, null=False, blank=False)
    description = models.TextField(_("Descrição"), null=False, blank=False)
    release_year = models.PositiveSmallIntegerField(_("Ano de Lançamento"), null=True, blank=True)
    amount_track = models.PositiveSmallIntegerField(_("Quantidade de Faixas"), null=True, blank=True)
    cover = models.ImageField(_("Capa"), upload_to="images/covers/", null=False, blank=False)
    musician = models.ForeignKey("music.Musician", verbose_name=_("Músico"), on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug"), null=True)

    created_at = models.DateTimeField(_("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Data de Última Modificação"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Álbum"
        verbose_name_plural = "Álbuns"


class Song(models.Model):
    name = models.CharField(_("Nome"), max_length=50)
    duration = models.TimeField(_("Duração"), null=True, blank=True)
    album = models.ForeignKey("music.Album", verbose_name=_("Album"), on_delete=models.CASCADE)
    main = models.BooleanField(_("Principal?"), null=True, default=False)
    order = models.IntegerField(_("Ordem"))
    file = models.FileField(_("Arquivo"), upload_to="music/")

    created_at = models.DateTimeField(_("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Data de Última Modificação"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Música"
        verbose_name_plural = "Músicas"


class Post(models.Model):
    title = models.CharField(_("Título da postagem"), max_length=50)
    text = models.TextField(_("Texto"), blank=True, null=True)
    image = models.ImageField(_("Imagem"), upload_to="posts/images", blank=True, null=True)
    musician = models.ForeignKey("music.Musician", verbose_name=_("Músico"), on_delete=models.CASCADE)

    created_at = models.DateTimeField(_("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Data de Última Modificação"), auto_now=True)

    def __str__(self):
        return f"{str(self.musician)} - {str(self.id)}"

    class Meta:
        verbose_name = "Postagem"
        verbose_name_plural = "Postagens"
