# Generated by Django 5.0.6 on 2024-06-01 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_user_gid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bucket',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
