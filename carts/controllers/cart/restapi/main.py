from django.conf import settings
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from carts.models import Cart
from carts.models.cart.serializers import CartSerializer
from carts.utils.cart.cart_manager import CartManager
from common_core.api.DefaultAPIView import DefaultAPIView
from common_core.model_objects.instance_update import instance_update


class CartAPI(DefaultAPIView):
    permission_module = "cart"
    model = Cart
    serializer = CartSerializer

    def get(self, request, *args, **kwargs):
        cart_manager = CartManager()
        if not request.session.get(settings.CART_ID, None):
            cart_manager.create()

        cart_in_session = cart_manager.get_cart_in_session()

        try:
            cart_in_db = Cart.objects.get(id=cart_in_session['id'])
        except Cart.DoesNotExist:
            cart_manager.create()
            cart_in_db = cart_manager.get_cart_in_db()
        except TypeError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = {
            'session': cart_in_session,
            'db': CartSerializer(cart_in_db).data
        }

        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        cart_manager = CartManager()

        data = request.data
        cart_manager.json_to_db(data)

        serializer = {
            'session': cart_manager.get_cart_in_session(),
            'db': CartSerializer(cart_manager.get_cart_in_db()).data
        }

        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        cart_manager = CartManager()
        cart_manager.destroy(request=request)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs: {
            "action": add/subtract/remove,
            "product": id,
            "quantity": n > 0 (optional)
        }
        :return:
        """
        cart_manager = CartManager()
        data = request.data.get('data')
        action = data.get("action")
        product = data.get("product")
        quantity = data.get("quantity", 1)

        result = cart_manager.update(
            action=action,
            product=product,
            quantity=quantity
        )

        if result:
            serializer = {
                'session': cart_manager.get_cart_in_session(),
                'db': CartSerializer(cart_manager.get_cart_in_db()).data
            }

            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
