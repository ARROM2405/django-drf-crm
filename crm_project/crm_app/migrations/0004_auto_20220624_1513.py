# Generated by Django 3.2.13 on 2022-06-24 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0003_auto_20220624_0540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='product_FK',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='web_FK',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='web_name',
        ),
        migrations.AlterField(
            model_name='lead',
            name='processed_at',
            field=models.DateTimeField(null=True, verbose_name='Lead processed date and time'),
        ),
    ]
