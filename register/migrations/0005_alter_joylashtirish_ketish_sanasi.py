# Generated by Django 4.2.1 on 2023-05-21 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_alter_joylashtirish_ketish_sanasi_alter_tolov_izoh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joylashtirish',
            name='ketish_sanasi',
            field=models.DateField(blank=True, null=True),
        ),
    ]
