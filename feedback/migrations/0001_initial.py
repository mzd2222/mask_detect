# Generated by Django 3.2.9 on 2021-11-23 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback_table',
            fields=[
                ('feedback_id', models.IntegerField(primary_key=True, serialize=False)),
                ('feedback_msg', models.CharField(max_length=100)),
                ('feedback_time', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'feedback_table',
            },
        ),
    ]
