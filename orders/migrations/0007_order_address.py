# Generated by Django 2.2.4 on 2019-08-30 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_item_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='Pickup', max_length=200),
        ),
    ]
