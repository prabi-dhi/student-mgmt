# Generated by Django 5.1.3 on 2024-11-20 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_student_class_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
