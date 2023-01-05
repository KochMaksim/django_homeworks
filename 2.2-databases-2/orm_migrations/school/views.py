from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    object_list = Student.objects.all().order_by('group').prefetch_related('teachers')

    # for student in object_list:
    #     student_teachers = student.teachers.all()
    #     print(f'student_teachers: {student_teachers}')
        # for pos in student_teachers:
        #     print(f'pos: {pos}')
        #     print(f'teacher: {pos.name}')

    context = {
        'object_list': object_list,
    }

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'

    return render(request, template, context)
