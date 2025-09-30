from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from collects.models import Collection
from collects.constants import CACHE_KEY_PREFIX
from payments.models import Payment
from api.tasks import send_collection_created_email, send_payment_created_email


def clear_collection_cache(collect_id):
    cache_key = f"{CACHE_KEY_PREFIX}{collect_id}"
    cache.delete(cache_key)
    cache.delete(CACHE_KEY_PREFIX)


@receiver([post_save, post_delete], sender=Collection)
def collection_changed(sender, instance, **kwargs):
    clear_collection_cache(instance.id)


@receiver([post_save, post_delete], sender=Payment)
def like_changed(sender, instance, **kwargs):
    clear_collection_cache(instance.collect.id)


@receiver(post_save, sender=Collection)
def send_email_to_author(sender, instance, created, **kwargs):
    if created:
        send_collection_created_email.delay(collect_id=instance.id)


@receiver(post_save, sender=Payment)
def send_email_to_payer(sender, instance, created, **kwargs):
    if created:
        send_payment_created_email.delay(payment_id=instance.id)


# @receiver(post_save, sender=Payment)
# def make_inactive_collect(sender, instance, **kwargs):
#     collect = instance.collect
#     current_sum = collect.payments.aggregate(Sum("amount"))["amount__sum"] or 0
#     if current_sum > collect.total_amount:
#         collect.is_active = False
#         collect.save(update_fields=["is_active"])
