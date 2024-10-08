# Generated by Django 5.0.6 on 2024-07-09 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_message_contact_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('image', models.ImageField(default='images/avatar.jpeg', upload_to='notifications/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
