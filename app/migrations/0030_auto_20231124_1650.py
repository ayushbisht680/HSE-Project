# Generated by Django 3.2.21 on 2023-11-24 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0029_auto_20231124_1301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hseusers',
            options={'verbose_name': 'HSE Users', 'verbose_name_plural': 'HSE Users'},
        ),
        migrations.AddField(
            model_name='generalhse',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='generalhse',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_general_hse_records', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generalhse',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='generalhse',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='updated_general_hse_records', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hse',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_hse_records', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hse',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='updated_hse_records', to='auth.user'),
            preserve_default=False,
        ),
    ]
