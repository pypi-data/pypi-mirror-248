from django.db.models.signals import post_save
from django.dispatch import receiver
from easy_thumbnails.signals import thumbnail_created
from filer.models import Image as FilerImage
from .utils import generate_thumbnails, store_as_webp


@receiver(post_save, sender=FilerImage)
def image_optimizer(sender, instance, **kwargs):
    try:
        print(f"Signal fired: [image_optimizer] for image [{instance}]")
        store_as_webp(instance, **kwargs)
        generate_thumbnails(instance, **kwargs)
    except Exception as e:
        print(f"Signal Exception: {e}")


@receiver(thumbnail_created)
def store_thumbnail_as_webp(sender, **kwargs):
    try:
        print(f"Signal fired: [store_thumbnail_as_webp] for image [{sender.name}]")
        store_as_webp(sender)
    except Exception as e:
        print(f"Signal Exception: {e}")
