from django.urls import path
from .views import index, paymentе

app_name = 'subscribe_payment'

urlpatterns = [
    path('', index, name='index'),
    path('payment/<int:id>/', paymentе, name='payment'),
]



