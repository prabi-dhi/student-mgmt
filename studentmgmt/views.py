from django.shortcuts import render, redirect
from django.http import HttpResponse
from teacher.models import Teacher
from student.models import Student
from subject.models import Subject
from classroom.models import Classroom
from user.models import User
from user.forms import UserForm
from teacher.forms import TeacherForm
from student.forms import StudentForm
from subject.forms import SubjectForm
from classroom.forms import ClassroomForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm

def is_admin(user):
    return user.user_type == 'ADMINISTRATION'
def is_student(user):
    return user.user_type == 'STUDENT'
def is_teacher(user):
    return user.user_type == 'TEACHER'

@user_passes_test(is_admin, login_url='/')
def register_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():           
            user = form.save()
            if user.user_type == 'TEACHER':
                Teacher.objects.create(user = user , name = user)
            elif user.user_type == 'STUDENT':
                Student.objects.create(user = user, s_name = user)
            return redirect('/base/')
        else:
            form = UserForm()      
    context={'form':form}
    return render(request,'register.html', context)

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():              
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username = email)
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                if user.user_type == 'ADMINISTRATION':
                    return redirect('/base/') 
                elif user.user_type == 'STUDENT':
                    return redirect('/studentbase/')
                else:
                    return redirect('/teacherbase/')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)

@user_passes_test(is_admin, login_url='/')
def base(request):
    show_button = request.path != '/base'
    context = {'show_button': show_button}
    return render(request, "base.html",context)

def custom_logout(request):
    logout(request)
    return redirect('/')

def student_view(request):
    return render(request, 'student.html')

@user_passes_test(is_admin, login_url='/')
def student_view(request):
    students = Student.objects.filter(is_deleted = False)
    form = StudentForm() 
    context = {       
        'students': students,
        'form' : form
    }
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/student/')
    return render(request, "student.html",context)

@user_passes_test(is_admin, login_url='/')
def student_delete(request, id):  
    student = Student.objects.get(id=id, is_deleted = False)  
    student.is_deleted = True
    student.save()
    return redirect('/student/')
@user_passes_test(is_admin, login_url='/')
def student_edit(request, id):
    instance = Student.objects.get(id = id, is_deleted=False)
    edit_form = StudentForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        edit_form = StudentForm(request.POST, request.FILES, instance= instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('/student/')  
    # add_form = StudentForm()
    context = {
               'edit_form': edit_form,
            #    'form':add_form,
               'edit_instance':instance}
    return render(request, 'student.html',context)

@user_passes_test(is_admin, login_url='/')
def teacher_view(request):   
    teachers = Teacher.objects.filter(is_deleted = False)
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/teacher/')
        else:
            print(form.errors)
            # form = TeacherForm()
    context = {'form': form,
               'teachers':teachers}
    return render(request,'teacher.html',context)
@user_passes_test(is_admin, login_url='/')
def teacher_edit(request, id):
    instance = Teacher.objects.get(id = id, is_deleted=False)
    edit_form = TeacherForm(instance=instance)
    if request.method == 'POST':
        edit_form = TeacherForm(request.POST, request.FILES, instance= instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('/teacher/')  
    context = {
               'edit_form': edit_form,
               'edit_instance':instance}
    return render(request, 'teacher.html',context)
@user_passes_test(is_admin, login_url='/')
def teacher_delete(request, id):  
    teacher = Teacher.objects.get(id=id, is_deleted = False)  
    teacher.is_deleted = True
    teacher.save()
    return redirect('/teacher/')

@user_passes_test(is_admin, login_url='/')
def subject_view(request):   
    subjects = Subject.objects.filter(is_deleted = False)
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/subject/')
        else:
            print(form.errors)
    context = {'form': form,
               'subjects':subjects}
    return render(request,'subject.html',context)
@user_passes_test(is_admin, login_url='/')
def subject_edit(request, id):
    instance = Subject.objects.get(id = id, is_deleted=False)
    edit_form = SubjectForm(instance=instance)
    if request.method == 'POST':
        edit_form = SubjectForm(request.POST, instance= instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('/subject/')  
    # add_form = SubjectForm()
    context = {
               'edit_form': edit_form,
            #    'form':add_form,
               'edit_instance':instance}
    return render(request, 'subject.html',context)

@user_passes_test(is_admin, login_url='/')
def subject_delete(request, id):  
    subject = Subject.objects.get(id=id, is_deleted = False)  
    subject.is_deleted = True
    subject.save()
    return redirect('/subject/')

@user_passes_test(is_admin, login_url='/')
def classroom_view(request):   
    classrooms = Classroom.objects.filter(is_deleted = False)
    form = ClassroomForm()
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/classroom/')
        else:
            print(form.errors)
    context= {'form': form,
              'classrooms': classrooms}
    return render(request, 'classroom.html',context)

@user_passes_test(is_admin, login_url='/')
def classroom_edit(request, id):   
    instance = Classroom.objects.get(id = id, is_deleted=False)
    edit_form = ClassroomForm(instance=instance)
    if request.method == 'POST':
        edit_form = ClassroomForm(request.POST, instance= instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('/classroom/')  
    context = {
               'edit_form': edit_form,
               'edit_instance':instance}
    return render(request, 'classroom.html',context)
@user_passes_test(is_admin, login_url='/')
def classroom_delete(request, id):  
    classroom = Classroom.objects.get(id=id, is_deleted = False)  
    classroom.is_deleted = True
    classroom.save()
    return redirect('/classroom/')

@user_passes_test(is_student, login_url='/')
def student_base(request):
    user = request.user
    students= Student.objects.filter(user = user)
    return render(request,'studentbase.html',{'students':students})

@user_passes_test(is_teacher, login_url ='/')
def teacher_base(request):
    user = request.user
    teachers = Teacher.objects.filter(user=user)
    students = Student.objects.filter(is_deleted = False)
    context={'students':students,
             'teachers':teachers,
    }
    return render(request, 'teacherbase.html', context)

@user_passes_test(is_teacher, login_url ='/')
def teacher_base_edit(request, id):
    instance = Student.objects.get(id = id, is_deleted = False)
    form = StudentForm(instance=instance)
    if request.method == 'POST':
        form= StudentForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/teacherbase/')
    context={
             'form': form,
             'instance': instance
    }
    return render(request, 'teacherbase.html', context)

