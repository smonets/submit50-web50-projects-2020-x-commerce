# Generated by Django 4.0 on 2021-12-18 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo_url',
            field=models.URLField(default='nophoto.bmp'),
        ),
    ]