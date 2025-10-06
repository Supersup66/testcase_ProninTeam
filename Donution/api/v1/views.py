from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import (CollectionDetailSerializer,
                                CollectionSerializer, PaymentSerializer,
                                UserSerializer)
from collects.constants import CACHE_INSTANCE_KEY_PREFIX, CACHE_LIST_KEY_PREFIX
from collects.models import Collection
from collects.permissions import IsOwnerOrReadOnly

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

    @method_decorator(cache_page(60 * 5, key_prefix=CACHE_LIST_KEY_PREFIX))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5, key_prefix=CACHE_INSTANCE_KEY_PREFIX))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.validated_data['collect'] = collection
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
