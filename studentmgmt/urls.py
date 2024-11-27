from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.login_page, name = 'login_page'),
    path('base/', views.base, name = 'base'),
    path('register/', views.register_page, name= 'register_page'),
    path('logout/', views.custom_logout, name= 'logout'),
    path('student/', views.student_view, name='student_view'), 
    path('student_edit/<int:id>/', views.student_edit, name='student_edit'),
    path('student/delete/<int:id>/', views.student_delete, name='student_delete'),
    path('teacher/',views.teacher_view, name='teacher_view'),
    path('teacher_edit/<int:id>/', views.teacher_edit, name='teacher_edit'),
    path('teacher/delete/<int:id>/', views.teacher_delete, name='teacher_delete'),
    path('subject/', views.subject_view, name= 'subject_view'),
    path('subject/edit/<int:id>/', views.subject_edit, name ='subject_edit'),
    path('subject/delete/<int:id>/', views.subject_delete, name ='subject_delete'),
    path('classroom/', views.classroom_view, name = 'classroom_view'),
    path('classroom/edit/<int:id>/', views.classroom_edit, name='classroom_edit'),
    path('classroom/delete/<int:id>/', views.classroom_delete, name = 'classroom_delete'),
    path('marks/', views.marks_view, name='marks_view'),
    path('marks/subject/<int:subject_id>/', views.marks_view_subject, name='marks_view_subject'),

    path('studentbase/', views.student_base, name = 'student_base'),
    path('teacherbase/', views.teacher_base, name= 'teacher_base'),
    path('teacher_grade/<int:id>/', views.teacher_grade, name = 'teacher_grade'),
    path('teacher_grade_edit/<int:id>/', views.teacher_grade_edit, name='teacher_grade_edit'),
    path('studentbase/edit/<int:id>/', views.student_base_edit, name = 'student_base_edit'),
    # path(r'^password/$', views.change_password, name='change_password'),
    path('student_marksheet/<int:id>', views.student_marksheet, name = 'student_marksheet'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
