# Generated by Django 4.0 on 2021-12-17 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='Listings', to='auctions.Category'),
        ),
    ]
