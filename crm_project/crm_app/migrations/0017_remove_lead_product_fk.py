# Generated by Django 3.2.13 on 2022-06-27 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0016_lead_product_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='product_FK',
        ),
    ]