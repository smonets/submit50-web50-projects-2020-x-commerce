# Generated by Django 4.0 on 2021-12-17 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_category_listing_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
