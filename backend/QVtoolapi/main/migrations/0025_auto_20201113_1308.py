# Generated by Django 3.1.2 on 2020-11-13 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20201113_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='matching_fund',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10),
        ),
    ]
