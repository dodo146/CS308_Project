# Generated by Django 4.1.7 on 2023-06-09 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0016_orderedproduct_purchased_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedproduct',
            name='InstockID',
            field=models.IntegerField(default=0),
        ),
    ]
