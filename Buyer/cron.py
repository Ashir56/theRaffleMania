import logging
from .models import BuyerCard
import stripe
from RaffleMania import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.core.mail import send_mail
logger = logging.getLogger(__name__)
from django.utils.translation import gettext_lazy as _


def process():
    cards = BuyerCard.objects.all()
    if cards:
        for card in cards:
            stripe.Charge.create(
                amount=4400 * 100,
                currency="usd",
                customer=card.token,
                description="My First Test Charge (created for API docs)",
            )
    print("Seller Charges Deducted")
    print("HELLO")


def send_email():
    send_mail(
        subject="Email From Cronjob",
        message="I am sending this email via cronjob you will get it every 2 minutes",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["a4aliahmad123@gmail.com", "rijepe9732@saturdata.com", "shahidmuneerawan@gmail.comp"]
    )
    print("Email Sent")
