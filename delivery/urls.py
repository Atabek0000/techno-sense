from django.urls import path
from .views import DeliveryCostView

urlpatterns = [
    path('calculate/', DeliveryCostView.as_view(), name='calculate_delivery_cost'),
]