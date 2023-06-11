from django.contrib import admin
from .models import Cart,PurchaseHistory,Refund
# Register your models here.

admin.site.register(Cart)
admin.site.register(PurchaseHistory)
admin.site.register(Refund)