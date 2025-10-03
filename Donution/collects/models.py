from django.db import models as m
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from collects.constants import (
    TITLE_MAX_LENGTH,
    TEXT_FIELD_MAX_LENGHT,
    REASON_MAX_LENGTH,
    MAX_TARGET_AMOUNT,
    MIN_TARGET_AMOUNT,
    Reason
)

User = get_user_model()


class Collection(m.Model):

    author = m.ForeignKey(
        User,
        on_delete=m.CASCADE,
        verbose_name=_('Author')
    )

    title = m.CharField(
        _('Collect description'),
        max_length=TITLE_MAX_LENGTH
    )
    description = m.TextField(
        _('Collect description'),
        max_length=TEXT_FIELD_MAX_LENGHT
    )
    reason = m.CharField(
        _('Reason of collection'),
        max_length=REASON_MAX_LENGTH,
        choices=Reason.choices
    )
    target_amount = m.IntegerField(
        verbose_name=_('Collection amount'),
        validators=[
            MinValueValidator(MIN_TARGET_AMOUNT),
            MaxValueValidator(MAX_TARGET_AMOUNT)
        ],
        null=True,
        blank=True,
        default=None,
    )
    image = m.ImageField(
        _('Collection image'),
        upload_to='collection/images/',
        null=True,
        blank=True,
        default=None,
    )
    created_at = m.DateTimeField(
        _('Date of creation'),
        auto_now_add=True
    )

    end_time = m.DateTimeField(
        _('End date collection'),
        default=None,
        null=True,
        blank=True
    )
    is_active = m.BooleanField(
        _('Is active collection'),
        default=True
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
        Returns the total sum of all payments associated with this collection.
        """
        return int(self.payments.aggregate(
            total_amount=m.Sum('amount'))['total_amount'] or 0)
