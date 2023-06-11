from django.db import models
from Product.models import Users,InStockProduct,PurchasedProduct
from django.utils import timezone
# Create your models here.
class Cart(models.Model):
    product = models.ForeignKey(InStockProduct,related_name="cart_product",on_delete=models.CASCADE)
    user = models.ForeignKey(Users,related_name="cart_product",on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} added by {self.user}"

class PurchaseHistory(models.Model):
    ID = models.IntegerField(primary_key=True,unique=True,default=0)
    product = models.ForeignKey(PurchasedProduct,related_name="purchase_history",on_delete=models.CASCADE)
    user = models.ForeignKey(Users,related_name="purchase_history",on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    refund_requested = models.BooleanField(verbose_name='Refund Requested',default=False)
    refund_accepted = models.BooleanField(verbose_name='Refund Accepted',default=False)

    class Meta:
        verbose_name_plural = "Purchase Histories"

    def __str__(self) -> str:
        return f"{self.product} purchased by {self.user}"
    

class Refund(models.Model):
    ID = models.IntegerField(primary_key=True,unique=True,default=0)
    product = models.ForeignKey(PurchasedProduct,related_name="refund",on_delete=models.CASCADE)
    user = models.ForeignKey(Users,related_name="refund",on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    Approved = models.BooleanField(verbose_name='Approved',default=False)

    class Meta:
        verbose_name_plural = "Refunds"

    def __str__(self) -> str:
        return f"Refund requested by {self.user}"