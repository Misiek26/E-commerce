# Generated by Django 5.1.2 on 2025-01-15 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.cartitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.order')),
            ],
        ),
    ]
