# Generated by Django 4.2.1 on 2023-06-29 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0017_tolov_tolangan_summa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tolov',
            name='tolangan_summa',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
