# Generated by Django 4.1 on 2024-06-08 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_studenddt_hoten'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenddt',
            name='hoten',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]