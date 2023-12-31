# Generated by Django 3.2.18 on 2023-06-24 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeketIsraelApp', '0014_leket_db_24_06'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leket_db_24_06',
            name='ground_temp',
            field=models.CharField(max_length=100, null=True, verbose_name='ground_temp'),
        ),
        migrations.AlterField(
            model_name='leket_db_24_06',
            name='max_temp',
            field=models.CharField(max_length=100, null=True, verbose_name='max_temp'),
        ),
        migrations.AlterField(
            model_name='leket_db_24_06',
            name='min_temp',
            field=models.CharField(max_length=100, null=True, verbose_name='min_temp'),
        ),
    ]
