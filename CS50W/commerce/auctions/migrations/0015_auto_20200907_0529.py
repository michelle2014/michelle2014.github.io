# Generated by Django 3.0.8 on 2020-09-07 05:29

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_delete_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid_count',
            field=models.DecimalField(blank=True, decimal_places=0, default=Decimal('0.00'), max_digits=3, null=True),
        ),
    ]
