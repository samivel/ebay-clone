# Generated by Django 3.1 on 2020-08-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchers', to='auctions.Listing'),
        ),
    ]
