# Generated by Django 4.2.1 on 2023-05-21 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_joylashtirish_kelish_sanasi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joylashtirish',
            name='ketish_sanasi',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tolov',
            name='izoh',
            field=models.TextField(null=True),
        ),
    ]
