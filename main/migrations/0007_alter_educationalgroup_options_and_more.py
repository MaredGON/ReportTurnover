# Generated by Django 5.0.4 on 2024-04-24 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_laboratory_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='educationalgroup',
            options={'verbose_name': 'Группы', 'verbose_name_plural': 'Группы'},
        ),
        migrations.RemoveField(
            model_name='educationalgroup',
            name='title',
        ),
        migrations.AddField(
            model_name='educationalgroup',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='educationalgroup',
            name='number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер группы'),
        ),
    ]