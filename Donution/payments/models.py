from django.db import models as m
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from collects.models import Collection

User = get_user_model()


class Payment(m.Model):

    amount = m.DecimalField(
        _('Payment amount'),
        max_digits=10,
        decimal_places=2
    )
    collect = m.ForeignKey(Collection, on_delete=m.CASCADE)

    payer = m.ForeignKey(
        User,
        on_delete=m.SET_NULL,
        null=True
    )
    payment_date_time = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.payer.username} pay {self.amount} '
                f'to "{self.collect.title}"')
