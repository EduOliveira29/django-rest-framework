
from django.urls import include, path
from rest_framework import routers
from order import viewsets

router = routers.SimpleRouter()
router.register(r"order", viewsets.OrderViewSet, basename="order")

# GARANTA QUE ESSA LINHA EXISTE:
app_name = "order"

urlpatterns = [
    path("", include(router.urls)),
]