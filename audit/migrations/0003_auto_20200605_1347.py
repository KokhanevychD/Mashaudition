# Generated by Django 3.0.5 on 2020-06-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0002_auto_20200512_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playeraudit',
            name='action_number',
            field=models.CharField(max_length=255),
        ),
    ]