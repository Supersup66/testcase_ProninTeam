from django.db import models as m
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from collects.models import Collection
from collects.constants import (
    MAX_TARGET_AMOUNT,
    MIN_TARGET_AMOUNT

)
User = get_user_model()


class Payment(m.Model):

    amount = m.DecimalField(
        _('Payment amount'),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(MIN_TARGET_AMOUNT),
            MaxValueValidator(MAX_TARGET_AMOUNT)
        ],
    )
    collect = m.ForeignKey(Collection, on_delete=m.CASCADE)

    payer = m.ForeignKey(
        User,
        on_delete=m.SET_NULL,
        null=True
    )
    payment_date_time = m.DateTimeField(auto_now_add=True)

    is_hidden = m.BooleanField(default=False)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        default_related_name = 'payments'
        ordering = ('-payment_date_time',)

    def __str__(self):
        return (f'{self.payer.username} pay {self.amount} '
                f'to "{self.collect.title}"')
