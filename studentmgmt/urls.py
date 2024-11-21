"""
URL configuration for studentmgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_page, name= 'register_page'),
    path('login/', views.login_page, name = 'login_page'),
    path('', views.base, name = 'base'),
    path('logout/', views.custom_logout, name= 'logout'),
    path('student/', views.student_view, name='student_view'), 
    path('student_edit/<int:id>/', views.student_edit, name='student_edit'),
    path('student/delete/<int:id>/', views.student_delete, name='student_delete'),
    path('teacher/',views.teacher_view, name='teacher_view'),
    path('teacher_edit/<int:id>/', views.teacher_edit, name='teacher_edit'),
    path('teacher/delete/<int:id>/', views.teacher_delete, name='teacher_delete'),
    path('studentbase/', views.student_base, name = 'studentbase')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
