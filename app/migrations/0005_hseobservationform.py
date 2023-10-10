# Generated by Django 3.2.21 on 2023-10-08 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_finalsubmit'),
    ]

    operations = [
        migrations.CreateModel(
            name='HSEObservationForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SrNo', models.IntegerField()),
                ('Date', models.TextField(max_length=100)),
                ('Time', models.TextField(max_length=100)),
                ('Location', models.TextField(max_length=100)),
                ('PlantSite', models.TextField(max_length=100)),
                ('Observation', models.TextField(max_length=100)),
                ('UnsafeCondition', models.TextField(max_length=100)),
                ('Cateogry', models.TextField(max_length=100)),
                ('CorrrectiveActionTAken', models.TextField(max_length=100)),
                ('ResponsiblePerson', models.TextField(max_length=100)),
                ('ClosureDate', models.TextField(max_length=100)),
                ('Status', models.TextField(max_length=100)),
                ('StopWork', models.TextField(max_length=100)),
                ('OpenEvidence', models.FileField(null=True, upload_to='formUploads')),
                ('ClosedEvidence', models.FileField(null=True, upload_to='formUploads')),
                ('Remark', models.TextField(max_length=200)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.parentmodel')),
            ],
        ),
    ]
