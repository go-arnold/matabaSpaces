# Generated by Django 5.0.6 on 2024-06-26 15:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0007_cleaningservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoundObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('found_time', models.DateTimeField(auto_now_add=True)),
                ('is_claimed', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='found_objects/')),
                ('parking_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='park.parkingarea')),
            ],
        ),
    ]
