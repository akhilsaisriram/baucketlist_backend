# Generated by Django 5.0.6 on 2024-06-12 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members_feed', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='place',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
