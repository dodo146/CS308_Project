# Generated by Django 4.1.7 on 2023-06-09 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0018_purchasedproduct'),
        ('Cart', '0008_alter_cart_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasehistory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_history', to='Product.purchasedproduct'),
        ),
    ]