# Generated by Django 3.2.21 on 2023-12-14 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0065_auto_20231214_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalhse',
            name='promotional_activities_file',
            field=models.FileField(blank=True, null=True, upload_to='general_hse_files/'),
        ),
        migrations.AlterField(
            model_name='generalhse',
            name='today_day_worked_file',
            field=models.FileField(blank=True, null=True, upload_to='general_hse_files/'),
        ),
        migrations.AlterField(
            model_name='generalhse',
            name='toolbox_talk_manhours_file',
            field=models.FileField(blank=True, null=True, upload_to='general_hse_files/'),
        ),
        migrations.AlterField(
            model_name='hseobservation',
            name='hse_observation_file',
            field=models.FileField(blank=True, null=True, upload_to='hse_observation_files/'),
        ),
        migrations.AlterField(
            model_name='hsetraining',
            name='attendees_amplus_file',
            field=models.FileField(null=True, upload_to='hse_training_file/'),
        ),
        migrations.AlterField(
            model_name='hsetraining',
            name='attendees_contractor_file',
            field=models.FileField(null=True, upload_to='hse_training_file/'),
        ),
        migrations.AlterField(
            model_name='managementvisit',
            name='no_of_compilance_done_file',
            field=models.FileField(null=True, upload_to='management_visits/'),
        ),
        migrations.AlterField(
            model_name='managementvisit',
            name='no_of_management_visit_file',
            field=models.FileField(null=True, upload_to='management_visits/'),
        ),
        migrations.AlterField(
            model_name='managementvisit',
            name='total_finding_file',
            field=models.FileField(null=True, upload_to='management_visits/'),
        ),
        migrations.AlterField(
            model_name='stopwork',
            name='closed_evidence',
            field=models.FileField(null=True, upload_to='stop_work_file'),
        ),
        migrations.AlterField(
            model_name='stopwork',
            name='open_evidence',
            field=models.FileField(null=True, upload_to='stop_work_file'),
        ),
        migrations.AlterField(
            model_name='subincident',
            name='attach_report',
            field=models.FileField(null=True, upload_to='sub_incident_file'),
        ),
        migrations.AlterField(
            model_name='subobservation',
            name='closed_evidence_file',
            field=models.FileField(null=True, upload_to='sub_observation_files/'),
        ),
        migrations.AlterField(
            model_name='subobservation',
            name='open_evidence_file',
            field=models.FileField(null=True, upload_to='sub_observation_files/'),
        ),
    ]
