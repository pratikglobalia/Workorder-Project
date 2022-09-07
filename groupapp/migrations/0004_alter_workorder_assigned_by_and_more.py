# Generated by Django 4.1 on 2022-09-05 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groupapp', '0003_rename_desc_workorder_task_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='assigned_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='assigned_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='priority',
            field=models.CharField(blank=True, choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')], max_length=7),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('inprogres', 'inprogres'), ('complete', 'complete')], max_length=10),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='task_desc',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='task_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]