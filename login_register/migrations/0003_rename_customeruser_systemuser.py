# Generated by Django 3.2.9 on 2021-11-22 09:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('login_register', '0002_rename_systemuser_customeruser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerUser',
            new_name='SystemUser',
        ),
    ]
