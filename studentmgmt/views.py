from django.shortcuts import render, redirect
from django.http import HttpResponse
from teacher.models import Teacher
from student.models import Student
from subject.models import Subject
from classroom.models import Classroom
from user.models import User
from marks.models import Marks
from marks.forms import MarksForm
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
            # if user.exists():
            #     messages.error(request, "username exists")    
            #     return redirect('/login/')    
            user = form.save()
            if user.user_type == 'TEACHER':
                Teacher.objects.create(user = user , name = user)
            elif user.user_type == 'STUDENT':
                Student.objects.create(user = user, s_name = user)
            return redirect('/base/')
        else:
            # messages.error(request,"Account Creation Unsuccessful")
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
            student = form.save(commit=False) 
            user= User.objects.create(student=student, username = student.s_name, email=student.s_name.lower() + '@gmail.com')
            user.set_password(student.s_name)
            user.save()
            student.user = user
            student.save()
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
            teacher= form.save(commit=False)
            user= User.objects.create(teacher=teacher, username = teacher.name, user_type = "TEACHER", email=teacher.name.lower() + '@gmail.com')
            user.set_password(teacher.name)
            user.save()
            teacher.user = user
            teacher.save()
            return redirect('/teacher/')
        else:
            print(form.errors)
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


######## Marks

@user_passes_test(is_admin, login_url='/')
def marks_view(request):   
    marks = Marks.objects.filter(is_deleted = False)
    form = MarksForm()
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/marks/')
        else:
            print(form.errors)
    context= {'form': form,
              'marks': marks}
    return render(request, 'marks.html',context)

@user_passes_test(is_student, login_url='/')
def student_base(request):
    user = request.user
    students= Student.objects.filter(user = user)
    teachers = Teacher.objects.filter(is_deleted = False, class_assigned__in = [student.class_enrolled for student in students])

    context={
        'students':students,
        'teachers':teachers}
    return render(request,'studentbase.html',context)

def student_base_edit(request,id):
    user= request.user
    if request.method=='POST':
        new_email = request.POST.get('email')         
        if new_email == user.email:
            messages.error(request, "The email is already the same.")
            return redirect('/studentbase/')
        if User.objects.filter(email=new_email).exists():
            messages.error(request, "Email is already taken.")
            return redirect('/studentbase/')            
        try:
            user.email = new_email
            user.save()
            messages.success(request, "Email updated successfully.")
            return redirect('/studentbase/')
        except Exception as e:
            messages.error(request, "cant change email")
            return redirect('/studentbase/')
    
    return render(request,'studentbase.html')

@user_passes_test(is_teacher, login_url ='/')
def teacher_base(request):
    user = request.user
    teachers = Teacher.objects.filter(user=user)
    subjects = Subject.objects.filter(teacher_name__in = teachers)
    teacher_classes = [teacher.class_assigned for teacher in teachers]
    students = Student.objects.filter(is_deleted = False,class_enrolled__in=teacher_classes)

    marks = Marks.objects.filter(student__in=students, subject__in=subjects)

    context={'students':students,
             'teachers':teachers,
             'subjects':subjects,
             'marks':marks,
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

