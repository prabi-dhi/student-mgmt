from django.shortcuts import render, redirect
from teacher.forms import TeacherForm
from django.http import HttpResponse
from teacher.models import Teacher
from student.models import Student
from user.forms import UserForm
from user.models import User
from user.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from student.forms import StudentForm



# def teacher_image(request):
#     return render(request, 'teacher.html')

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
            return redirect('/register/')
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
                messages.success(request, 'logged in successfully')
                return redirect('/') 
            else:
                messages.error(request, 'User not found')
        else:
            messages.error(request, 'User not found')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)


@login_required(login_url='/login/')
def teacher_view(request):   
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('teacher')
        else:
            form = TeacherForm()
    context = {'form': form}
    return render(request,'teacher.html',context)

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

    

