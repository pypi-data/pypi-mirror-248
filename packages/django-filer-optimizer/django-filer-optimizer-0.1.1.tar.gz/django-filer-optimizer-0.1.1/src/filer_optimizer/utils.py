from django.conf import settings
from django.core.files import File
from django.db.models import Q, Subquery, OuterRef
from django.core.files.storage import default_storage
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.models import Thumbnail
from io import BytesIO
from PIL import Image
from pathlib import Path

# import pillow_avif


def annotate_queryset_with_thumbnails(
    queryset,
    thumbnail_size,
    img_name="image",
    field_name=None,
    thumbnail_conf="default",
):
    """
    Used by views to annotate a queryset with thumbnail
    """
    width, height = settings.THUMBNAIL_ALIASES[thumbnail_conf][thumbnail_size]["size"]
    size_name = f"_{width}x{height}_"
    thumbnails_subquery = Subquery(
        Thumbnail.objects.filter(
            Q(source__id=OuterRef(img_name))
            & Q(name__icontains=settings.THUMBNAIL_PREFIX)
            & Q(name__icontains=size_name),
        ).values("name")[:1]
    )
    if field_name:
        return queryset.annotate(**{field_name: thumbnails_subquery})
    else:
        return queryset.annotate(thumbnail=thumbnails_subquery)


def generate_thumbnails(instance, thumbnail_conf="default", **kwargs):
    """
    Used to generate all thumbanils with sizes configured inside the THUMBNAIL_ALIASES settings
    """
    try:
        print(f"Function: [generate_thumbnails] for image [{instance}]")
        thumbnailer = get_thumbnailer(f"{instance.file}")
        for x_key in settings.THUMBNAIL_ALIASES[thumbnail_conf].keys():
            thumbnail_options = settings.THUMBNAIL_ALIASES[thumbnail_conf][x_key]
            if not thumbnailer.get_existing_thumbnail(thumbnail_options):
                thumbnailer.get_thumbnail(thumbnail_options)
    except Exception as e:
        print(f"Function Exception: {e}")


def store_as_webp(instance, **kwargs):
    """
    Used to convert and store a saved image also in webp format
    """
    try:
        instance_filename = instance.file.name
        if not instance_filename:
            instance_filename = instance.name
        print(f"Function: [store_as_webp] for image [{instance_filename}]")
        if not default_storage.exists(instance_filename):
            raise FileNotFoundError(f"File not found! [{instance_filename}]")

        suffix = Path(instance_filename).suffix
        if suffix == ".webp":
            raise AttributeError(f"File is already a webp! [{instance_filename}]")
        new_path = str(Path(instance_filename).with_suffix(f"{suffix}.webp"))
        # print(f"New file name with webp suffix [{new_path}]")

        # Opening the image
        file = default_storage.open(instance_filename, "rb")
        # print(f"Open file from default storage [{file}]")
        image = Image.open(file)
        buffer = BytesIO()
        # print(f"File read from default storage and buffer opened")

        # Converting the image to RGB colour
        image = image.convert("RGB")

        # Saving the image as a different file inside buffer
        image.save(buffer, "webp", optimize=True, quality=95)
        # print(f"File saved inside buffer")

        # Save the buffer data through the storage backend
        file_object = File(buffer)
        file_object.content_type = "image/webp"
        default_storage.save(new_path, file_object)
        # print(f"File saved inside default storage")

        # # Check difference from original
        # orig_image = Image.open(file)
        # new_file = default_storage.open(new_path, 'rb')
        # new_image = Image.open(new_file)
        # print(f"File original format=[{orig_image.format}] size=[{orig_image.size}] mode=[{orig_image.mode}] bytes=[{file.size}]")
        # print(f"File converted format=[{new_image.format}] size=[{new_image.size}] mode=[{new_image.mode}] bytes=[{buffer.tell()}]")

    except Exception as e:
        print(f"Function Exception: {e}")


def store_as_avif(instance, **kwargs):
    """
    Used to convert and store a saved image also in avif format
    """
    try:
        instance_filename = instance.file.name
        if not instance_filename:
            instance_filename = instance.name
        print(f"Function: [store_as_avif] for image [{instance_filename}]")
        if not default_storage.exists(instance_filename):
            raise FileNotFoundError(f"File not found! [{instance_filename}]")

        suffix = Path(instance_filename).suffix
        if suffix == ".avif":
            raise AttributeError(f"File is already a webp! [{instance_filename}]")

        new_path = str(Path(instance_filename).with_suffix(f"{suffix}.avif"))
        # print(f"New file with avif suffix [{new_path}]")

        # Opening the image
        file = default_storage.open(instance_filename, "rb")
        # print(f"File open from default storage [{file}]")
        image = Image.open(file)
        buffer = BytesIO()
        # print(f"File read from default storage and buffer opened ...")

        # Converting the image to RGB colour
        image = image.convert("RGB")

        # Saving the image as a different file inside buffer
        image.save(buffer, "avif", optimize=True, quality=60)
        # print(f"File saved inside buffer...")

        # Save the buffer data through the storage backend
        file_object = File(buffer)
        file_object.content_type = "image/avif"
        default_storage.save(new_path, file_object)
        # print(f"File saved inside default storage ...")

        # Check difference from original
        # new_file = default_storage.open(new_path, 'rb')
        # new_image = Image.open(new_file)
        # print(f"File original format=[{image.format}] size=[{image.size}] mode=[{image.mode}] bytes=[{len(image.fp.read())}]")
        # print(f"File converted format=[{new_image.format}] size=[{new_image.size}] mode=[{new_image.mode}] bytes=[{len(new_image.fp.read())}]")

    except Exception as e:
        print(f"Function Exception: {e}")
