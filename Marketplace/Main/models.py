from django.db import models
from Product.models import Users

# Create your models here.


class Account(models.Model):
    ID = models.IntegerField(primary_key=True,unique=True,default=0)
    user = models.ForeignKey(Users,related_name="account",on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Accounts"

    def __str__(self) -> str:
        return f"Account for {self.user}"