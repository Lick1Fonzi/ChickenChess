# Generated by Django 4.1 on 2022-09-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='mode',
        ),
        migrations.AddField(
            model_name='game',
            name='moves',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
