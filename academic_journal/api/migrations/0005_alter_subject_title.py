# Generated by Django 5.1.3 on 2024-12-14 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_subject_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
