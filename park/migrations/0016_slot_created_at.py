# Generated by Django 5.0.6 on 2024-07-03 00:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0015_alter_foundobject_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
