# Generated by Django 3.1.7 on 2021-03-20 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion_board', '0003_auto_20210319_1818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='type',
            new_name='user_type',
        ),
    ]