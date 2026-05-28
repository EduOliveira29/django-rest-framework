import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(
            reverse("order:order-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        
        # CORREÇÃO: Removido o ["results"] pois a resposta vem como lista direta
        self.assertEqual(
            order_data[0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data[0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data[0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data[0]["product"][0]["category"][0]["title"],
            self.category.title,
        )
        # CORREÇÃO: Incluído o namespace 'order:' antes do nome da rota
        response = self.client.get(
            reverse("order:order-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data[0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data[0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data[0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data[0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        
        # Boa prática: Passar um dicionário direto e usar format="json" no client
        data = {"products_id": [product.id], "user": user.id}

        # CORREÇÃO: Incluído o namespace 'order:' antes do nome da rota
        response = self.client.post(
            reverse("order:order-list", kwargs={"version": "v1"}),
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)