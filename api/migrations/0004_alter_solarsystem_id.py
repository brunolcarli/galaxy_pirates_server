# Generated by Django 3.2.6 on 2025-05-03 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_ship_integrity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solarsystem',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
