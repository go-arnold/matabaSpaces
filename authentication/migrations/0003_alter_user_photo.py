# Generated by Django 5.0.6 on 2024-05-27 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_name_user_phone_number_user_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='images/parking.jpeg', null=True, upload_to='user_images/'),
        ),
    ]
