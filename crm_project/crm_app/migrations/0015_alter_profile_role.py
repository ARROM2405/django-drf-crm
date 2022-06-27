# Generated by Django 3.2.13 on 2022-06-27 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0014_remove_paymentstoweb_removed_user_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Operator', 'OP'), ('Stock manager', 'SM'), ('Payments executive', 'PE'), ('Administrator', 'AD'), ('Test role', 'TR')], default='Test role', max_length=30, verbose_name='Role'),
        ),
    ]
