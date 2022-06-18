# Generated by Django 3.2.13 on 2022-06-18 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0005_alter_web_web_api_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='id',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Invoice number'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sent_date',
            field=models.DateField(verbose_name='Send date for the order'),
        ),
    ]
