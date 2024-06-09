# Generated by Django 4.1 on 2024-06-03 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_diendan_diendancomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diendan',
            name='headline',
        ),
        migrations.RemoveField(
            model_name='diendan',
            name='sub_headline',
        ),
        migrations.AddField(
            model_name='diendan',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.studenddt'),
        ),
    ]