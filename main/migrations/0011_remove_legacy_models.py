from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0010_consolidate_merchant_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='merchant',
        ),
        migrations.RemoveField(
            model_name='location',
            name='merchant',
        ),
        migrations.RemoveField(
            model_name='logo',
            name='merchant',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Logo',
        ),
    ] 