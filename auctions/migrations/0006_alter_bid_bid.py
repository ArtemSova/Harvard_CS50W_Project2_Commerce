# Generated by Django 4.2.4 on 2023-08-07 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_alter_listing_starting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(default=0),
        ),
    ]
