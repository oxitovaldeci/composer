from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string

import string
import sys

from .models import Musician, Album
from composer_utils import squarify, cprint


@receiver(pre_save, sender=Musician)
def musician_before_saving(sender, instance, **kwargs):
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(instance.name)

    aux = squarify(instance.image)
    instance.image = InMemoryUploadedFile(
        aux,
        "ImageField",
        instance.image.name,
        "image,jpeg",
        sys.getsizeof(aux),
        None
    )


@receiver(pre_save, sender=Album)
def album_before_saving(sender, instance, **kwargs):
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(instance.name)

    aux = squarify(instance.cover)
    instance.cover = InMemoryUploadedFile(
        aux,
        "ImageField",
        instance.cover.name,
        "image,jpeg",
        sys.getsizeof(aux),
        None
    )
