# Generated by Django 5.0.6 on 2024-07-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0022_delete_notifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foundobject',
            name='image',
            field=models.ImageField(default='images/avatar.png', upload_to='found_objects/'),
        ),
    ]
