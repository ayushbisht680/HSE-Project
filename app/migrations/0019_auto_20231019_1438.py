# Generated by Django 3.2.21 on 2023-10-19 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20231018_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalsubmit',
            name='parent',
        ),
        migrations.DeleteModel(
            name='ListOfObservers',
        ),
        migrations.DeleteModel(
            name='FinalSubmit',
        ),
    ]
