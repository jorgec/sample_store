from typing import Dict

from django.conf import settings
from django.db import IntegrityError

from accounts.models import Account
from carts.models import Cart, CartItem
from carts.models.cart.constants import CartStateConstants
from carts.utils.cart.cart_constants import CartUpdateActions
from products.models import Product


class CartManager:
    cart: Dict
    request = None

    user: Account

    _is_prepped = False

    def __init__(self, *args, **kwargs):
        self.prep()
        try:
            self.cart = self.request.session[settings.CART_ID]
        except KeyError:
            self.create()
        except AttributeError:
            self.create()

    def attach_user(self):

        try:
            user = Account.objects.get(id=self.request.user.id)
        except AttributeError:
            from common_core.middleware.thread_local_middleware import get_current_user
            try:
                user = get_current_user().id
            except AttributeError:
                user = None
        except Account.DoesNotExist:
            user = None

        self.user = user

    def prep(self):
        from common_core.middleware.thread_local_middleware import get_current_request
        self.request = get_current_request()
        self.attach_user()

    def get_cart_in_db(self):
        try:
            return Cart.objects.get(id=self.cart['id'])
        except Cart.DoesNotExist:
            self.create()
        except TypeError:
            self.create()
        except AttributeError:
            return None

    def get_cart_in_session(self):
        from common_core.middleware.thread_local_middleware import get_current_request
        request = get_current_request()
        try:
            cart = request.session[settings.CART_ID]
        except KeyError:
            cart = None
        if not cart:
            self.create()
            if hasattr(self, "cart"):
                cart = request.session[settings.CART_ID]
        return cart

    def put_cart_in_session(self, cart):
        from common_core.middleware.thread_local_middleware import get_current_request
        request = get_current_request()
        request.session[settings.CART_ID] = cart

    # CRUD OPERATIONS

    def create_cart_object(self, user):
        cart_obj = Cart.objects.create(
            user=self.user
        )
        return cart_obj

    def create(self, *args, **kwargs):
        self.prep()

        if self.user:
            # check for open carts
            try:
                cart_obj = Cart.objects.get(
                    user_id=self.user,
                    status=CartStateConstants.OPEN
                )
            except Cart.DoesNotExist:
                cart_obj = self.create_cart_object(user=self.user)
            cart = {
                'id': str(cart_obj.id),
                'user': str(self.user.id),
            }

            self.cart = cart
            self.put_cart_in_session(self.cart)

            return cart_obj
        return None
        # else:
        #     cart_obj = self.create_cart_object(user=None)

    def json_to_db(self, data):
        self.prep()
        cart = self.get_cart_in_db()

        CartItem.objects.filter(cart=cart).delete()

        for item in data:
            product = item['product']['id']

            cart_item = CartItem.objects.create(
                cart=cart,
                product_id=product,
                quantity=item['quantity']
            )

    def destroy(self, *args, **kwargs):
        self.prep()

        try:
            self.request.session[settings.CART_ID] = None
            self.cart = {}
        except KeyError:
            pass

    def update(self, *args, **kwargs):
        self.prep()
        success = False
        cart = self.get_cart_in_db()

        action = kwargs.get('action', CartUpdateActions.ADD)

        quantity = kwargs.get('quantity', 1)

        try:
            _q = quantity - 0
        except TypeError:
            raise ValueError(f"Invalid quantity: {quantity}")

        if quantity < 1:
            raise ValueError(f"Invalid quantity: {quantity}")

        if action == CartUpdateActions.ADD:
            try:
                product = Product.objects.get(id=kwargs.get('product'))
            except Product.DoesNotExist:
                raise ValueError("Product does not exist!")

            try:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity
                )
                success = True
            except IntegrityError:
                cart_item = CartItem.objects.get(
                    cart=cart,
                    product=product
                )

                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
                success = True
        elif action == CartUpdateActions.SET:
            try:
                product = Product.objects.get(id=kwargs.get('product'))
            except Product.DoesNotExist:
                raise ValueError("Product does not exist!")

            try:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity
                )
                success = True
            except IntegrityError:
                cart_item = CartItem.objects.get(
                    cart=cart,
                    product=product
                )

                cart_item.quantity = quantity
                cart_item.save()
                success = True
        elif action == CartUpdateActions.SUB:
            try:
                product = Product.objects.get(id=kwargs.get('product'))
            except Product.DoesNotExist:
                raise ValueError("Product does not exist!")

            try:
                cart_item = CartItem.objects.get(
                    cart=cart,
                    product=product
                )

                if cart_item.quantity - quantity < 0:
                    cart_item.delete()
                else:
                    cart_item.quantity = cart_item.quantity - quantity
                    cart_item.save()
                success = True

            except CartItem.DoesNotExist:
                raise ValueError("Item does not exist!")
        elif action == CartUpdateActions.REMOVE:
            try:
                product = Product.objects.get(id=kwargs.get('product'))
            except Product.DoesNotExist:
                raise ValueError("Product does not exist!")

            try:
                cart_item = CartItem.objects.get(
                    cart=cart,
                    product=product
                )

                cart_item.delete()
                success = True

            except CartItem.DoesNotExist:
                raise ValueError("Item does not exist!")
        elif action == CartUpdateActions.CLOSE:
            cart.status = CartStateConstants.CLOSED
            cart.save()
            success = True
        else:
            raise ValueError(f"Unsupported action: {action}")

        return success

    def search_cart_item(self, needle, haystack):
        for key, item in enumerate(haystack):
            if item['id'] == needle:
                return key
        return None

    def __update(self, *args, **kwargs):
        self.prep()
        update_session = True

        action = kwargs.get('action', CartUpdateActions.ADD)
        product = kwargs.get('product')
        quantity = kwargs.get('quantity', 1)

        try:
            _q = quantity - 0
        except TypeError:
            raise ValueError(f"Invalid quantity: {quantity}")

        if quantity < 1:
            raise ValueError(f"Invalid quantity: {quantity}")

        cart = self.get_cart_in_session()
        data = cart['data']['cart_items']

        if action == CartUpdateActions.ADD:
            key = self.search_cart_item(product, data)
            if key:
                data[key]['quantity'] = cart[key]['quantity'] + 1
            else:
                data.append(
                    {
                        'id': product,
                        'quantity': 1
                    }
                )
        elif action == CartUpdateActions.SET:
            key = self.search_cart_item(product, data)
            if key:
                data[key]['quantity'] = quantity
            else:
                data.append(
                    {
                        'id': product,
                        'quantity': quantity
                    }
                )
        elif action == CartUpdateActions.SUB:
            key = self.search_cart_item(product, data)
            if key:
                if data[key]['quantity'] - quantity <= 1:
                    del (data[key])
                else:
                    data[key]['quantity'] = cart[key]['quantity'] - 1

        elif action == CartUpdateActions.REMOVE:
            key = self.search_cart_item(product, data)
            if key:
                del (data[key])

        elif action == CartUpdateActions.CLOSE:
            _cart = self.get_cart_in_db()
            _cart.status = CartStateConstants.CLOSED
            _cart.save()
            update_session = False

        else:
            raise ValueError(f"Unsupported action: {action}")

        if update_session:
            cart['data']['cart_items'] = data
            self.cart = cart
        else:
            self.cart = self.get_cart_in_db()

        self.put_cart_in_session(self.cart)
