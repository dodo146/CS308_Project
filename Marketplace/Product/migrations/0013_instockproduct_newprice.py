# Generated by Django 4.1.7 on 2023-05-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_alter_instockproduct_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='instockproduct',
            name='newPrice',
            field=models.IntegerField(default=0),
        ),
    ]
