# Generated by Django 3.2.21 on 2023-12-11 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0052_remove_hse_plant_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HSEUsers',
            new_name='HSEUser',
        ),
        migrations.RenameField(
            model_name='generalhse',
            old_name='committe_meetings',
            new_name='committee_meetings',
        ),
        migrations.RenameField(
            model_name='hseobservation',
            old_name='hse_observation',
            new_name='hse_observation_file',
        ),
        migrations.RenameField(
            model_name='hsetrainingsmodel',
            old_name='no_of_attendees_amplus',
            new_name='attendees_amplus_file',
        ),
        migrations.RenameField(
            model_name='hsetrainingsmodel',
            old_name='no_of_attendees_contractor',
            new_name='attendees_contractor_file',
        ),
        migrations.AlterField(
            model_name='generalhse',
            name='hse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.hse'),
        ),
        migrations.AlterField(
            model_name='generalhse',
            name='submittedDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='hse',
            name='formSubmittedDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='hse_observation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.hseobservation'),
        ),
        migrations.AlterField(
            model_name='hseobservationform',
            name='responsible_person',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hsetrainingsmodel',
            name='hse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.hse'),
        ),
    ]
