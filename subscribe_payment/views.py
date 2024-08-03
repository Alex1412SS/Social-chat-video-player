from django.shortcuts import render, redirect
import uuid

from django.urls import reverse
from yookassa import Configuration, Payment
from .models import lvl_subscribe
from account.models import Profile
# Create your views here.
def index(request):
    return render(request, 'subs/subscribe.html')

def paymentе(request, id):
    lvl_subscrib = lvl_subscribe.objects.get(id=id)
    Configuration.account_id = "Your account id"
    Configuration.secret_key = "Your secret key"

    idempotence_key = uuid.uuid4()

    payment = Payment.create({
        "amount": {
            "value": lvl_subscrib.price,
            "currency": 'RUB',

        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(reverse('toons:index')),

        },

        "capture": True,
        "test": True,
        "description": lvl_subscrib.name,
    }, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url
    payment_successful = payment.status
    print(payment.json())



    if payment_successful == "succeeded" or 'success':
        profile = Profile.objects.get(user=request.user)
        profile.sub = lvl_subscrib
        profile.save()

    return redirect(confirmation_url)