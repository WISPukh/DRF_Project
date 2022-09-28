from shop.models import Product
from .models import Order, OrderItem
from django.db.models import F


class CartActionsService:
    def add_product_to_cart(self, request):
        product = self.get_object()  # noqa
        user_pk = request.user.pk
        quantity = int(request.data['quantity'])

        order, is_order_created = Order.objects.get_or_create(
            customer_id_id=user_pk,
            status='CART'
        )

        snapshot_item, is_snapshot_created = OrderItem.objects.get_or_create(
            customer_id_id=user_pk,
            unit_price=product.price,
            product_id=product,
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

    def change_products_in_cart(self, request):
        order = self.get_object()  # noqa

        products_in_db = order.product.through.objects.all()
        products_in_request = request.data['product']

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
            if value == quantity_data_in_db[key]:
                continue
            to_update[key] = value

        quantity_data_to_add = {
            product['product_id']: product['quantity']
            for product in products_in_request
            if product['product_id'] in to_add
        }

        # update database's info
        products_to_update = OrderItem.objects.filter(
            product_id__in=to_update.keys()
        )
        for product in products_to_update:
            product.quantity = to_update[product.product_id_id]
        OrderItem.objects.bulk_update(products_to_update, ['quantity'])

        # delete products
        OrderItem.objects.filter(product_id__in=to_delete).delete()

        # add products
        products_to_add_to_cart = Product.objects.filter(pk__in=to_add)

        # unfortunately, bulk_create is not possible for m2m
        for product in products_to_add_to_cart:
            item = OrderItem.objects.create(
                order_id=order,
                unit_price=product.price,
                product_id=product,
                product_name=product.name,
                quantity=quantity_data_to_add[product.pk],
                customer_id_id=request.user.pk
            )
            order.product.add(item)
        return order
