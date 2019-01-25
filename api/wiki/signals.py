from django.dispatch import receiver
from django.db.models import signals

from .models import (
    PageModel,
    VersionModel
)


@receiver(signals.post_save, sender=PageModel)
def create_version_for_new_page(sender, created, instance, update_fields, **kwargs):

    if created:
        VersionModel.objects.create(
            text=instance.text,
            page_id=instance.id
        )
