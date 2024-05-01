# Generated by Django 4.2.6 on 2024-04-28 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_comments_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='listing_comment',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='particular_comments',
        ),
        migrations.AddField(
            model_name='auction_listings',
            name='comment',
            field=models.ManyToManyField(to='auctions.comments'),
        ),
    ]