# Generated by Django 5.0.6 on 2024-10-11 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_user_email_alter_user_username'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='users',
        ),
    ]
