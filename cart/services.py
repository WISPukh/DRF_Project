from django.db.models import F
from django.db.transaction import atomic

from shop.models import Product
from shop.utils import generate_json_error_response
from .models import Order, OrderItem
from .tasks import send_mail_of_order


class OrderAmountExceededError(Exception):
    pass


class CartActionsService:
    def __init__(self, user, request_data, product=None, order=None):
        self.product = product
        self.order = order
        self.user = user
        self.request_data = request_data

    @atomic
    def add_product_to_cart(self):
        quantity = int(self.request_data.get('quantity'))

        order, is_order_created = Order.objects.get_or_create(
            customer_id_id=self.user.pk,
            status='CART'
        )

        snapshot_item, is_snapshot_created = OrderItem.objects.get_or_create(
            customer_id_id=self.user.pk,
            unit_price=self.product.price,
            product_name=self.product.name,
            product_id=self.product,
            order_id=order
        )
        order.product.add(snapshot_item)

        if is_order_created and is_snapshot_created:
            snapshot_item.quantity = quantity
        else:
            snapshot_item.quantity = F('quantity') + quantity

        snapshot_item.save()
        order.save()
        order.refresh_from_db()
        return order

    @atomic
    def change_products_in_cart(self):
        products_in_db = self.order.product.through.objects.all()
        products_in_request = self.request_data.get('cart')

        # making sets
        pk_products_in_db = {item.orderitem.product_id_id for item in products_in_db}
        pk_in_request = {item['product_id'] for item in products_in_request}
        to_delete = pk_products_in_db.difference(pk_in_request)
        to_add = pk_in_request - to_delete - pk_products_in_db
        to_change = pk_products_in_db.intersection(pk_in_request)

        # making dicts
        quantity_data_in_db = {
            product.orderitem.product_id_id: product.orderitem.quantity
            for product in products_in_db
            if product.orderitem.product_id_id in to_change
        }

        quantity_data_in_request = {
            product['product_id']: product['quantity']
            for product in products_in_request
            if product['product_id'] in to_change
        }

        to_update = dict()
        for key, value in quantity_data_in_request.items():
            if value != quantity_data_in_db[key]:
                to_update[key] = value

        # update database's info
        if to_update:
            products_to_update = OrderItem.objects.filter(
                product_id__in=to_update.keys()
            )
            for product in products_to_update:
                product.quantity = to_update[product.product_id_id]
            OrderItem.objects.bulk_update(products_to_update, ['quantity'])

        # delete products
        if to_delete:
            OrderItem.objects.filter(product_id__in=to_delete).delete()

        # add products
        if to_add:
            products_to_add_to_cart = Product.objects.filter(pk__in=to_add)

            quantity_data_to_add = {
                product['product_id']: product['quantity']
                for product in products_in_request
                if product['product_id'] in to_add
            }

            # unfortunately, bulk_create is not possible for m2m
            for product in products_to_add_to_cart:
                item = OrderItem.objects.create(
                    order_id=self.order,
                    unit_price=product.price,
                    product_id=product,
                    product_name=product.name,
                    quantity=quantity_data_to_add[product.pk],
                    customer_id_id=self.user.pk
                )
                self.order.product.add(item)
        return self.order

    @atomic
    def make_order(self):
        city = self.request_data.get('city')
        address = self.request_data.get('address')
        if not (city and address):
            return generate_json_error_response(message='You can not make an order without city or address')

        products_in_cart = self.order.orderitem_set.all()
        pks_products_in_cart = {product.product_id_id for product in products_in_cart}
        products_from_stock = Product.objects.filter(pk__in=pks_products_in_cart)

        for index, item in enumerate(products_from_stock):
            if item.in_stock < products_in_cart[index].quantity or 1 > products_in_cart[index].quantity:
                return generate_json_error_response(message='incorrect amount of products in cart')

        self.order.city = city
        self.order.address = address
        self.order.total_price = self.order.calculated_total_price
        self.order.total_amount = self.order.calculated_total_amount
        self.order.status = 'CREATED'
        self.order.save()
        send_mail_of_order.delay(self.order.pk)
        return self.order
