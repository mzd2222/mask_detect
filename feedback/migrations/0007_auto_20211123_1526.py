# Generated by Django 3.2.9 on 2021-11-23 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0006_alter_feedback_table_feedback_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='feedback_table',
            new_name='feedbacks',
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_msg', models.CharField(max_length=100)),
                ('comment_time', models.DateTimeField(auto_now=True)),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.feedbacks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comments_table',
            },
        ),
    ]
