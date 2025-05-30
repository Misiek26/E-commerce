# Generated by Django 5.1.2 on 2024-10-22 19:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_clientprofile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientprofile',
            name='phone',
            field=models.CharField(error_messages={'unique': 'Ten numer telefonu jest już zarejestrowany. Proszę podać inny numer.'}, max_length=9, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='Proszę wprowadzić poprawny numer telefonu.', regex='^\\d{9}$')]),
        ),
    ]
