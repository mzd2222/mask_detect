# Generated by Django 3.2.9 on 2021-11-23 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_rename_user_id_feedback_table_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback_table',
            name='feedback_id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
