"""
Middleware to hold Cart reference
"""

from carts.utils.cart.cart_manager import CartManager


class CartMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cart = CartManager()
        request.cart = cart.get_cart_in_db()

        return self.get_response(request)
