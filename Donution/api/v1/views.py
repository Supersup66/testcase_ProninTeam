from rest_framework.viewsets import ModelViewSet
from api.v1.serializers import (
    CollectionSerializer,
    PaymentSerializer,
    UserSerializer
)
from collects.models import Collection
from payments.models import Payment
from django.contrib.auth import get_user_model
from django.core.cache import cache
from api.utils import delete_cache

from rest_framework.response import Response

User = get_user_model()


class CollectionViewSet(ModelViewSet):

    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    CACHE_KEY_PREFIX = "collection-view"

    def list(self, request):
        result = cache.get(self.CACHE_KEY_PREFIX)
        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            cache.set(self.CACHE_KEY_PREFIX, result, 600)
        else:
            print('Cache retrieved!')

        result = self.serializer_class(result, many=True)

        return Response(result.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response


class PaymentViewSet(ModelViewSet):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
