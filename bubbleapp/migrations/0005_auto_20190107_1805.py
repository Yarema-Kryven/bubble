# Generated by Django 2.1.4 on 2019-01-07 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bubbleapp', '0004_auto_20181231_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]