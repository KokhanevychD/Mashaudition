# Generated by Django 3.0.5 on 2020-05-11 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_played', models.DateTimeField()),
                ('action', models.CharField(max_length=255)),
                ('action_number', models.BigIntegerField()),
                ('game', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=5)),
                ('summary', models.FloatField()),
                ('s_coins', models.IntegerField()),
                ('t_money', models.FloatField()),
                ('w_money', models.FloatField()),
                ('cashier', models.FloatField()),
                ('get_s_coins', models.IntegerField()),
                ('t_money_cashier', models.FloatField()),
                ('w_money_cashier', models.FloatField()),
                ('action_type', models.CharField(default='', max_length=20)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit', to='player.Player')),
            ],
            options={
                'ordering': ['date_played'],
            },
        ),
    ]
