# Generated by Django 4.2.1 on 2023-07-05 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0020_alter_tolov_tolangan_summa_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]