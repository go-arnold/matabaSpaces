# Generated by Django 5.0.6 on 2024-07-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='images/avatar.png', upload_to='user_images/'),
        ),
    ]
