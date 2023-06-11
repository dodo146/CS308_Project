from django.urls import path
from . import views
from .forms import LoginForm


urlpatterns = [
    path("login/",views.login,name = "login"),
    path("",views.index,name="index"),
    path("logout",views.logout_view,name = "logout"),
    path("signup/",views.signup,name = "signup"),
    path("delivery",views.delivery,name="delivery"),
    path("purchased",views.purchased,name="purchased_items"),
    path("account/",views.accounts,name = "account")
]
