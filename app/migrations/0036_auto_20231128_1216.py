# Generated by Django 3.2.21 on 2023-11-28 06:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20231128_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hseobservationform',
            name='date',
        ),
        migrations.RemoveField(
            model_name='hseobservationform',
            name='sr_no',
        ),
        migrations.RemoveField(
            model_name='hseobservationform',
            name='time',
        ),
        migrations.AddField(
            model_name='hseobservationform',
            name='datetime_observation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='category',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='closure_date',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='corrective_action_taken',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='location',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='observation',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='plant_site',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='remark',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='responsible_person',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='status',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='stop_work',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='unsafe_condition',
            field=models.CharField(max_length=300),
        ),
    ]
