# Generated by Django 5.0.6 on 2024-07-27 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_merchant_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='province',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='town',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
