from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from collects.models import Collection
from payments.models import Payment


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'title',
        'description',
        'reason',
        'target_amount',
        'image',
        'created_at',
        'end_time',
        'is_active'
    )
    list_display_links = ('id',)
    search_fields = ('title',)
    list_filter = ('reason', 'is_active', 'target_amount')
    empty_value_display = _('Not defined',)
    autocomplete_fields = ('author',)
    readonly_fields = ('created_at',)
    ordering = ('-id',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'collect',
        'payer',
        'payment_date_time',
        'is_hidden'
    )
    list_display_links = ('id',)
    list_filter = ('amount', 'collect', 'payer', 'is_hidden')
    empty_value_display = _('Not defined',)
    autocomplete_fields = ('payer', 'collect')
    readonly_fields = ('payment_date_time', 'is_hidden')
    ordering = ('-id',)
