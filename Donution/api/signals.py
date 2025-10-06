import os

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.tasks import send_collection_created_email, send_payment_created_email
from api.v1.utils import delete_cache
from collects.constants import CACHE_INSTANCE_KEY_PREFIX, CACHE_LIST_KEY_PREFIX
from collects.models import Collection
from payments.models import Payment


@receiver([post_save, post_delete], sender=Collection)
def collection_changed(sender, instance, **kwargs):
    delete_cache(CACHE_LIST_KEY_PREFIX)
    delete_cache(CACHE_INSTANCE_KEY_PREFIX)


@receiver([post_save], sender=Payment)
def payment_changed(sender, instance, **kwargs):
    delete_cache(CACHE_LIST_KEY_PREFIX)
    delete_cache(CACHE_INSTANCE_KEY_PREFIX)


@receiver(post_save, sender=Collection)
def send_email_to_author(sender, instance, created, **kwargs):
    if created:
        send_collection_created_email.delay(collect_id=instance.id)


@receiver(post_save, sender=Payment)
def send_email_to_payer(sender, instance, created, **kwargs):
    if created:
        send_payment_created_email.delay(payment_id=instance.id)


@receiver(post_save, sender=Payment)
def make_inactive_collect(sender, instance, **kwargs):
    collect = instance.collect
    if collect.target_amount and (
            collect.get_total_amount() > collect.target_amount):
        collect.is_active = False
        collect.save()


@receiver(post_delete, sender=Collection)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
