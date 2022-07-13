# Generated by Django 3.2.13 on 2022-06-30 04:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0019_alter_order_lead_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_in_delivery',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Products in delivery to clients'),
        ),
    ]