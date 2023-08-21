from django.db.models.signals import post_save
from django.dispatch import receiver

from flowerapp.models import Order
from courierbot import send_order


@receiver(post_save, sender=Order)
def send_orders(sender, instance, created, **kwargs):
    if created:
        send_order(instance)