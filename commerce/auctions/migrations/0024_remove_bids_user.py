# Generated by Django 4.2.6 on 2024-05-05 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_alter_bids_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='user',
        ),
    ]