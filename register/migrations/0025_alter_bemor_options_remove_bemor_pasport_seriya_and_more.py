# Generated by Django 4.2.1 on 2023-08-03 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0024_bemor_tugilgan_sana'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bemor',
            options={'ordering': ['familiya', 'ism']},
        ),
        migrations.RemoveField(
            model_name='bemor',
            name='pasport_seriya',
        ),
        migrations.AlterField(
            model_name='bemor',
            name='sharif',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
