# Generated by Django 5.1.3 on 2024-11-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_alter_teacher_department_alter_teacher_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]