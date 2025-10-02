# from django.utils.translation import gettext_lazy as _
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
        amount = attrs.get('amount')
        if collect.target_amount:
            remains = collect.target_amount - collect.get_total_amount()
            if amount > remains:
                raise s.ValidationError(
                    'Your payment exceeds the remaining amount to be '
                    f'collected. It remains to collect {remains} ₽.')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['payer'] = self.context['request'].user
        return Payment.objects.create(**validated_data)


class CollectionSerializer(s.ModelSerializer):

    # payments = PaymentSerializer(many=True, required=False)

    author = UserSerializer(read_only=True, default=s.CurrentUserDefault())

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
