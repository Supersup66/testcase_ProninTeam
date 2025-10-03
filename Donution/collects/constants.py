from django.db import models as m
from django.utils.translation import gettext_lazy as _


TEXT_FIELD_MAX_LENGHT = 255
REASON_MAX_LENGTH = 30
TITLE_MAX_LENGTH = 50
CACHE_KEY_PREFIX = "collection_view_"


class Reason(m.TextChoices):
    """Payments types."""

    BIRTHDAY = 'BIRTHDAY', _('Birthday')
    WEDDING = 'WEDDING', _('Wedding')
    CHARITY = 'CHARITY', _('Charity')
    THERAPY = 'THERAPY', _('Therapy')
    FUNERAL = 'FUNERAL', _('Funeral')
    DONUTS = 'DONUTS', _('Donuts')


MAX_PAGE_SIZE = 100
PAGE_SIZE = 20
PAGE_QUERY_PARAM = 'page'
PAGE_SIZE_QUERY_PARAM = 'page_size'

MIN_TARGET_AMOUNT = 1
MAX_TARGET_AMOUNT = 1000_000_000
