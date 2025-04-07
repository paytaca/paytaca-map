from django.db import migrations, models

def migrate_data(apps, schema_editor):
    Merchant = apps.get_model('main', 'Merchant')
    Location = apps.get_model('main', 'Location')
    Category = apps.get_model('main', 'Category')
    Logo = apps.get_model('main', 'Logo')

    # Migrate location data using raw SQL
    for location in Location.objects.all():
        schema_editor.execute(
            """
            UPDATE main_merchant 
            SET landmark = %s,
                location = %s,
                street = %s,
                town = %s,
                city = %s,
                province = %s,
                state = %s,
                country = %s,
                longitude = %s,
                latitude = %s
            WHERE id = %s
            """,
            [
                location.landmark,
                location.location,
                location.street,
                location.town,
                location.city,
                location.province,
                location.state,
                location.country,
                location.longitude,
                location.latitude,
                location.merchant_id
            ]
        )

    # Migrate category data using raw SQL
    for category in Category.objects.all():
        schema_editor.execute(
            "UPDATE main_merchant SET category = %s WHERE id = %s",
            [category.category, category.merchant_id]
        )

    # Migrate logo data using raw SQL
    for logo in Logo.objects.all():
        schema_editor.execute(
            "UPDATE main_merchant SET logo_size = %s, logo_url = %s WHERE id = %s",
            [logo.size, logo.url, logo.merchant_id]
        )

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0009_delete_vault'),
    ]

    operations = [
        # Add new fields to Merchant
        migrations.AddField(
            model_name='merchant',
            name='landmark',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='street',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='town',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='province',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='country',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='longitude',
            field=models.DecimalField(decimal_places=10, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='latitude',
            field=models.DecimalField(decimal_places=10, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='category',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='logo_size',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='logo_url',
            field=models.URLField(null=True),
        ),
        
        # Run data migration
        migrations.RunPython(migrate_data),
    ] 