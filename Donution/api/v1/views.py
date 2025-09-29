from rest_framework.viewsets import ModelViewSet
from api.v1.serializers import (
    CollectionSerializer,
    PaymentSerializer,
    UserSerializer
)
from collects.models import Collection
from payments.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()


class CollectionViewSet(ModelViewSet):

    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()


class PaymentViewSet(ModelViewSet):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
