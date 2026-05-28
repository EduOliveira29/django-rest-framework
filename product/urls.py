from django.urls import include, path
from rest_framework import routers
from product import viewsets

router = routers.SimpleRouter()
router.register(r"category", viewsets.CategoryViewSet, basename="category")
router.register(r"product", viewsets.ProductViewSet, basename="product")

# GARANTA QUE ESSA LINHA EXISTE:
app_name = "product"

urlpatterns = [
    path("", include(router.urls)),
]