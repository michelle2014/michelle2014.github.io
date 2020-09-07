# Generated by Django 3.0.8 on 2020-09-07 05:31

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20200907_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid_count',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3),
        ),
    ]
