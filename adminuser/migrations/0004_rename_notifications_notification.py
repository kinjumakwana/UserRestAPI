# Generated by Django 4.1.4 on 2022-12-29 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("adminuser", "0003_notifications"),
    ]

    operations = [
        migrations.RenameModel(old_name="Notifications", new_name="Notification",),
    ]
