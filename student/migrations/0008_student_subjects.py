# Generated by Django 5.1.3 on 2024-11-26 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_student_table'),
        ('subject', '0003_alter_subject_sub_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(to='subject.subject'),
        ),
    ]
