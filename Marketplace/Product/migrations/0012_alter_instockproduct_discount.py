# Generated by Django 4.1.7 on 2023-05-30 11:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0011_instockproduct_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instockproduct',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]