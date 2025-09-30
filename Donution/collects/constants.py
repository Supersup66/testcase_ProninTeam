from django.db import models as m
from django.utils.translation import gettext_lazy as _


TEXT_FIELD_MAX_LENGHT = 255
REASON_MAX_LENGTH = 30
CACHE_KEY_PREFIX = "collection_view_"


class Reason(m.TextChoices):
    """Payments types."""

    BIRTHDAY = 'BIRTHDAY', _('Birthday')
    WEDDING = 'WEDDING', _('Wedding')
    CHARITY = 'CHARITY', _('Charity')
    THERAPY = 'THERAPY', _('Therapy')
    FUNERAL = 'FUNERAL', _('Funeral')
    DONUTS = 'DONUTS', _('Donuts')
