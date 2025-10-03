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
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.select_related('author'
                                                 ).prefetch_related('payments')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return CollectionDetailSerializer
        elif self.action == 'payments':
            return PaymentSerializer
        return CollectionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request):
        result = cache.get(CACHE_KEY_PREFIX)
        if not result:
            result = self.get_queryset()
            cache.set(CACHE_KEY_PREFIX, result, 600)
        result = self.get_serializer(result, many=True)

        return Response(result.data)

    def retrieve(self, request, *args, **kwargs):
        collection_id = kwargs['pk']
        cache_key = f'{CACHE_KEY_PREFIX}{collection_id}'
        result = cache.get(cache_key)
        if not result:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            cache.set(cache_key, serializer.data, 600)
            result = serializer.data
        return Response(result)

    @action(
        methods=['post'],
        detail=True,
        url_path='payments',
        permission_classes=(IsAuthenticated,)
    )
    def payments(self, request, *args, **kwargs):
        """Provides payment to collection."""

        collection = self.get_object()
        request.data['collect'] = collection.id
        serializer = self.get_serializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.validated_data["collect"] = collection
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
