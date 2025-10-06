import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers as s

from collects.constants import MAX_TARGET_AMOUNT, MIN_TARGET_AMOUNT, Reason
from collects.models import Collection
from payments.models import Payment

User = get_user_model()


class Base64ImageField(s.ImageField):
    """Decodes an image from Base64 format into a file."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            title = self.context['request'].data['title'][:10]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=title + '.' + ext
            )
        return super().to_internal_value(data)


class UserSerializer(s.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        ref_name = 'ApiV1UserSerializer'


class PaymentSerializer(s.ModelSerializer):

    payer = UserSerializer(read_only=True, default=s.CurrentUserDefault())

    payment_date_time = s.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = Payment
        exclude = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_hidden:
            data['amount'] = 'Hidden'
        return data

    def validate(self, attrs):
        collect = attrs.get('collect')
        if not collect.is_active:
            raise s.ValidationError(
                _('You can\'t pay for this collection. Collection completed!'))
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['payer'] = self.context['request'].user
        return Payment.objects.create(**validated_data)


class CollectionSerializer(s.ModelSerializer):

    image = Base64ImageField(
        required=False,
        allow_null=False,
        allow_empty_file=False
    )

    author = UserSerializer(read_only=True, default=s.CurrentUserDefault())

    end_time = s.DateTimeField(format='iso-8601', required=False)

    collected_amount = s.SerializerMethodField()

    payer_count = s.SerializerMethodField()

    reason = s.ChoiceField(
        choices=Reason.choices)

    target_amount = s.IntegerField(required=False,)

    class Meta:
        model = Collection
        exclude = ('created_at', 'is_active')

    def get_collected_amount(self, obj):
        return obj.get_total_amount()

    def get_payer_count(self, obj):
        return obj.payments.all().count()

    def validate_end_time(self, value):
        if value < now():
            raise s.ValidationError(_('End time must be in future!'))
        return value

    def validate_target_amount(self, value):
        if MIN_TARGET_AMOUNT > value > MAX_TARGET_AMOUNT:
            raise s.ValidationError(
                _('Target amount must between '
                  f'{MIN_TARGET_AMOUNT}..{MAX_TARGET_AMOUNT}'))
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return Collection.objects.create(**validated_data)


class CollectionDetailSerializer(CollectionSerializer):

    payments = PaymentSerializer(many=True, required=False)

    link_to_pay = s.SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'

    def get_link_to_pay(self, obj):
        return self.context.get('request').build_absolute_uri() + 'payments/'
