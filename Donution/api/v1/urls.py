from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.v1.views import CollectionViewSet

app_name = "api_v1"
api_v1 = DefaultRouter()


api_v1.register(r'collections', CollectionViewSet, basename='collections')


urlpatterns = [
    path('', include(api_v1.urls)),
]
