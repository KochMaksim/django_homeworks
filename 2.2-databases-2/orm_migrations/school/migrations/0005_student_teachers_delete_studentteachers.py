# Generated by Django 4.1.3 on 2022-12-09 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_remove_student_teachers_studentteachers'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='teachers',
            field=models.ManyToManyField(related_name='students', to='school.teacher'),
        ),
        migrations.DeleteModel(
            name='StudentTeachers',
        ),
    ]
