# Generated by Django 3.2.6 on 2021-08-05 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='unique_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
