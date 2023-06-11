from django.urls import path
from . import views

urlpatterns = [
    path("",views.cart,name="cart"),
    path("buy/",views.buy,name="buy"),
    path("card_info",views.card_info, name="card_info")

]
