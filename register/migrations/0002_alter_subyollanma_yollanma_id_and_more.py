# Generated by Django 4.2.1 on 2023-09-07 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subyollanma',
            name='yollanma_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='register.yollanma'),
        ),
        migrations.AlterField(
            model_name='tolov',
            name='subyollanma_idlar',
            field=models.ManyToManyField(blank=True, null=True, to='register.subyollanma'),
        ),
    ]