# Generated by Django 5.0.4 on 2024-04-17 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_laboratory_status_lecturer_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratory_status',
            name='student_status',
            field=models.CharField(blank=True, default='Не сгенерировал QR', max_length=50, null=True),
        ),
    ]
