# Generated by Django 5.1.2 on 2025-01-15 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_delete_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_method',
            field=models.CharField(default='ok', max_length=15),
            preserve_default=False,
        ),
    ]
