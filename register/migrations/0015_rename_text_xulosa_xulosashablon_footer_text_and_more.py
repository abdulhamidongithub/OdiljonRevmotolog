# Generated by Django 4.2.1 on 2023-06-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0014_alter_tolov_ozgartirilgan_sana'),
    ]

    operations = [
        migrations.RenameField(
            model_name='xulosashablon',
            old_name='text_xulosa',
            new_name='footer_text',
        ),
        migrations.AddField(
            model_name='xulosashablon',
            name='header_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]