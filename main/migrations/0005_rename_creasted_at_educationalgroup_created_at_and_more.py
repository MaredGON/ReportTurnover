# Generated by Django 5.0.4 on 2024-04-21 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_laboratory_status_student_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educationalgroup',
            old_name='creasted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='laboratory',
            old_name='creasted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='laboratory_status',
            old_name='creasted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='lecturer',
            old_name='creasted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='lecturersubject',
            old_name='creasted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='creasted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='creasted_at',
            new_name='created_at',
        ),
    ]