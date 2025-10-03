from django.utils.translation import gettext_lazy as _
from rest_framework import serializers as s
from django.contrib.auth import get_user_model

from collects.models import Collection
from collects.constants import Reason
from payments.models import Payment

User = get_user_model()


class UserSerializer(s.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class PaymentSerializer(s.ModelSerializer):

    payer = UserSerializer(read_only=True, default=s.CurrentUserDefault())

    payment_date_time = s.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = Payment
        exclude = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_hidden:
            data['amount'] = "Hidden"
        return data

    def validate(self, attrs):
        collect = attrs.get('collect')
        if not collect.is_active:
            raise s.ValidationError(_('Collection completed!'))
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['payer'] = self.context['request'].user
        return Payment.objects.create(**validated_data)


class CollectionSerializer(s.ModelSerializer):

    author = UserSerializer(read_only=True, default=s.CurrentUserDefault())

    end_time = s.DateTimeField(format='iso-8601')

    created_at = s.DateTimeField(read_only=True, format='iso-8601')

    collected_amount = s.SerializerMethodField()

    payer_count = s.SerializerMethodField()

    reason = s.ChoiceField(
        choices=Reason.choices)

    class Meta:
        model = Collection
        fields = '__all__'

    def get_collected_amount(self, obj):
        return obj.get_total_amount()

    def get_payer_count(self, obj):
        return obj.payments.all().count()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return Collection.objects.create(**validated_data)


class CollectionDetailSerializer(CollectionSerializer):

    payments = PaymentSerializer(many=True, required=False)

    link = s.SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'

    def get_link(self, obj):
        return self.context.get('request').build_absolute_uri()
