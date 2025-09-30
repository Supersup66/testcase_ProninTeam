from django.db import models as m
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from collects.constants import TEXT_FIELD_MAX_LENGHT, Reason, REASON_MAX_LENGTH
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models import Sum


User = get_user_model()


class Collection(m.Model):

    author = m.ForeignKey(User, on_delete=m.CASCADE)

    title = m.CharField(
        'Collect description',
        max_length=TEXT_FIELD_MAX_LENGHT
    )
    description = m.TextField(
        'Collect description',
        max_length=TEXT_FIELD_MAX_LENGHT
    )
    reason = m.CharField(
        verbose_name=_('Reason of collection'),
        max_length=REASON_MAX_LENGTH,
        choices=Reason.choices
    )
    target_amount = m.PositiveSmallIntegerField(
        _('Collection amount'),
        blank=True,
        null=True
    )
    image = m.ImageField(
        _('Collection image'),
        upload_to='collection/images/',
        null=True,
        blank=True,
        default=None,
    )
    created_at = m.DateTimeField(
        verbose_name=_('Date of creation'),
        auto_now_add=True
    )

    end_time = m.DateTimeField(
        verbose_name=_('End date collection'),
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')
        default_related_name = 'collections'
        ordering = ('-created_at',)

    def get_total_amount(self):
        """
        Возвращает общую сумму всех платежей, связанных с этой коллекцией.
        """
        return self.payments.aggregate(
            total_amount=Sum('amount'))['total_amount'] or 0


@receiver(post_delete, sender=Collection)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
