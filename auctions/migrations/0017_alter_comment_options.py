# Generated by Django 4.0 on 2021-12-21 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': 'Comments'},
        ),
    ]
