# Generated by Django 5.0.6 on 2024-06-01 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_user_bucket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='spass',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
