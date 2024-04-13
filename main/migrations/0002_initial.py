# Generated by Django 5.0.4 on 2024-04-12 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Educational',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('surname2', models.CharField(blank=True, max_length=100, null=True)),
                ('key', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('surname2', models.CharField(blank=True, max_length=100, null=True)),
                ('chat', models.IntegerField(blank=True, null=True)),
                ('group', models.IntegerField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('group', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('educational', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.educational')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.lecturer')),
            ],
            options={
                'ordering': ['educational_id', 'created_at'],
            },
        ),
        migrations.AddField(
            model_name='educational',
            name='lecturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.lecturer'),
        ),
        migrations.CreateModel(
            name='Laboratory_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.laboratory')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.student')),
            ],
        ),
    ]
