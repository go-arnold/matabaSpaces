# Generated by Django 5.0.6 on 2024-08-03 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='user_images/avatar', upload_to='user_images/'),
        ),
    ]