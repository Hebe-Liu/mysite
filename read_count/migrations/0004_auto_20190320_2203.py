# Generated by Django 2.1.5 on 2019-03-20 14:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('read_count', '0003_auto_20190320_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
