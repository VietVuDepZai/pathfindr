# Generated by Django 4.1 on 2024-06-04 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_remove_diendan_headline_remove_diendan_sub_headline_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('khoihoc', models.CharField(blank=True, max_length=1900, null=True)),
                ('tester', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.studenddt')),
            ],
        ),
    ]
