# Generated by Django 3.2.6 on 2025-05-02 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_mission'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='integrity',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
