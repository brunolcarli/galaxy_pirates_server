# Generated by Django 3.2.6 on 2025-05-04 13:22

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0005_auto_20250504_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('fleet_count', models.IntegerField(default=0, null=True)),
                ('buildings', models.IntegerField(default=0, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='mission',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.usermodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planet',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.usermodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ship',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.usermodel'),
            preserve_default=False,
        ),
    ]
