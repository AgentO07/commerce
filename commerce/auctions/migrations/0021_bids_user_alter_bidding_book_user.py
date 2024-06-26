# Generated by Django 4.2.6 on 2024-05-05 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_rename_bid_bidding_book_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bidding_book',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bidding_book', to=settings.AUTH_USER_MODEL),
        ),
    ]
