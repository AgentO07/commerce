# Generated by Django 4.2.6 on 2024-05-05 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_bids_user_alter_bidding_book_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidding_book',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidding_book', to=settings.AUTH_USER_MODEL),
        ),
    ]
