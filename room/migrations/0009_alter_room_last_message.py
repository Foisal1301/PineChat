# Generated by Django 4.1 on 2022-08-24 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_alter_room_last_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='last_message',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
