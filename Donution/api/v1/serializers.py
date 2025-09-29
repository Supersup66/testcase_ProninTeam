# from django.utils.translation import gettext_lazy as _
from rest_framework import serializers as s
from django.contrib.auth import get_user_model

from collects.models import Collection
from payments.models import Payment

User = get_user_model()


class UserSerializer(s.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id',)


class CollectionSerializer(s.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'


class PaymentSerializer(s.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
