# Generated by Django 5.0.6 on 2025-04-11 03:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_merchant_category_merchant_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='merchant',
            options={'ordering': ['-last_transaction_date', '-last_update']},
        ),
        migrations.AddField(
            model_name='category',
            name='short_name',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_short_name', message='Short name must contain only alphanumeric characters with no spaces', regex='^[a-zA-Z0-9]+$')]),
            preserve_default=False,
        )
    ]
