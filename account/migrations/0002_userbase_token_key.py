# Generated by Django 4.0 on 2024-02-22 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='token_key',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
