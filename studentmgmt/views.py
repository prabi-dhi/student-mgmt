from django.shortcuts import render, redirect
from teacher.forms import TeacherForm
from django.http import HttpResponse
from teacher.models import Teacher
from student.models import Student
from subject.models import Subject
from user.forms import UserForm
from user.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from student.forms import StudentForm

def is_ADMINISTRATION(self):
    if str(self.user_type) == 'ADMINISTRATION':
        return True
    else:
        return False
ad_login_required = user_passes_test(lambda u: u.user_type == 'ADMINISTRATION', login_url ='/login/')

def admin_login_required(view_func):
    decorated_view_func = login_required(ad_login_required(view_func), login_url='/')
    return decorated_view_func

@admin_login_required
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
            return redirect('/')
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
                    return redirect('/') 
                else:
                    return redirect('/studentbase/')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)

@login_required(login_url = '/login/')
def base(request):
    return render(request, "base.html")

def custom_logout(request):
    logout(request)
    return redirect('/login/')

def student_view(request):
    return render(request, 'student.html')

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def student_delete(request, id):  
    student = Student.objects.get(id=id, is_deleted = False)  
    student.is_deleted = True
    student.save()
    return redirect('/student/')
@login_required(login_url='/login/')
def student_edit(request, id):
    instance = Student.objects.get(id = id, is_deleted=False)
    edit_form = StudentForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        edit_form = StudentForm(request.POST, request.FILES, instance= instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('/student/')  
    add_form = StudentForm()

    context = {
               'edit_form': edit_form,
               'form':add_form,
               'edit_instance':instance}
    return render(request, 'student.html',context)

@login_required(login_url='/login/')
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

def teacher_edit(request, id):
    instance = Teacher.objects.get(id = id, is_deleted=False)
    edit_form = TeacherForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        edit_form = TeacherForm(request.POST, request.FILES, instance= instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('/teacher/')  
    add_form = TeacherForm()

    context = {
               'edit_form': edit_form,
               'form':add_form,
               'edit_instance':instance}
    return render(request, 'teacher.html',context)
@login_required(login_url='/login/')
def teacher_delete(request, id):  
    teacher = Teacher.objects.get(id=id, is_deleted = False)  
    teacher.is_deleted = True
    teacher.save()
    return redirect('/teacher/')

def student_base(request):
    return render(request,'studentbase.html')




    

