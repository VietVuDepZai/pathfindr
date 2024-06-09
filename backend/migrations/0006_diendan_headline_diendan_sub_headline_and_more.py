# Generated by Django 4.1 on 2024-06-03 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_remove_diendan_thumbnail_alter_diendan_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='diendan',
            name='headline',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diendan',
            name='sub_headline',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='diendan',
            name='thumbnail',
            field=models.ImageField(blank=True, default='/images/placeholder.png', null=True, upload_to='images'),
        ),
    ]