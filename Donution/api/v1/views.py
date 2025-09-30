from rest_framework.viewsets import ModelViewSet
from api.v1.serializers import (
    CollectionDetailSerializer,
    CollectionSerializer,
    PaymentSerializer,
    UserSerializer
)
from collects.models import Collection
from collects.permissions import IsOwnerOrReadOnly
from collects.constants import CACHE_KEY_PREFIX
from payments.models import Payment
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response

User = get_user_model()


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return CollectionDetailSerializer

        return CollectionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request):
        result = cache.get(CACHE_KEY_PREFIX)
        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            cache.set(CACHE_KEY_PREFIX, result, 600)
        else:
            print('Cache retrieved!')

        result = self.get_serializer(result, many=True)

        return Response(result.data)

    def retrieve(self, request, *args, **kwargs):
        collection_id = kwargs['pk']
        cache_key = f'{CACHE_KEY_PREFIX}{collection_id}'
        result = cache.get(cache_key)
        if not result:
            print('Hitting DB')
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            cache.set(cache_key, serializer.data, 600)
            result = serializer.data
        else:
            print('Cache retrieved!')
        return Response(result)


class PaymentViewSet(ModelViewSet):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
