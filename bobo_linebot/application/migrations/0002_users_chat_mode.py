# Generated by Django 3.0.2 on 2020-02-05 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='chat_mode',
            field=models.CharField(default='none', max_length=50),
            preserve_default=False,
        ),
    ]
