from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from cart.models import Order


@shared_task
def send_mail_of_order(order_pk):
    order = Order.objects.get(pk=order_pk)
    return send_mail(
        f'Order № {order.pk}',
        "Your order content is:\n"
        f"Price: {order.total_price}\n"
        f"Total quantity: {order.total_amount}",
        settings.EMAIL_HOST_USER,
        [order.customer_id.email]
    )
