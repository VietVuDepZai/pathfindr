# Generated by Django 4.1 on 2024-06-03 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_diendan_headline_diendan_sub_headline_and_more'),
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
        migrations.RemoveField(
            model_name='diendan',
            name='thumbnail',
        ),
    ]