# Generated by Django 3.2.21 on 2023-12-12 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20231212_1105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stopwork',
            options={'verbose_name': 'Stop Work Form', 'verbose_name_plural': 'Stop Work Form'},
        ),
        migrations.RenameField(
            model_name='violationmemoform',
            old_name='date_field',
            new_name='stopwork_date',
        ),
    ]
