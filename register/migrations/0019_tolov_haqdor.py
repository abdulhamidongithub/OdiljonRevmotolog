# Generated by Django 4.2.1 on 2023-06-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0018_alter_tolov_tolangan_summa'),
    ]

    operations = [
        migrations.AddField(
            model_name='tolov',
            name='haqdor',
            field=models.BooleanField(default=False),
        ),
    ]