# Generated by Django 4.1 on 2022-08-21 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rating', models.IntegerField(default=500)),
                ('profileimg', models.ImageField(default='default.jpg', upload_to='')),
                ('lowest_rating', models.IntegerField(default=500)),
                ('highest_rating', models.IntegerField(default=500)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.TextField()),
                ('time', models.IntegerField()),
                ('increment', models.IntegerField()),
                ('Black', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Black', to='players.profile')),
                ('White', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='White', to='players.profile')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='players.profile')),
            ],
        ),
    ]