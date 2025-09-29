from api.v1 import urls
from django.urls import include, path

app_name = "api"

urlpatterns = [path("v1/", include(urls)),]
