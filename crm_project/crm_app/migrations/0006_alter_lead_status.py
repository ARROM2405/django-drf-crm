# Generated by Django 3.2.13 on 2022-06-24 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0005_auto_20220624_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='status',
            field=models.CharField(choices=[('Approved', 'AP'), ('Reject', 'RE'), ('Not processed', 'NP'), ('Not answered', 'NA')], default='NP', max_length=25, verbose_name='Lead status'),
        ),
    ]
