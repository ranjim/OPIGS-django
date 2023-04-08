from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from taggit.models import Tag
from .forms import *

def create_user(user_data, user_type, form_data):
    if user_type == 'S':
        new_user = Student.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
            roll_no=form_data['roll_no'],
            dept=form_data['dept'],
            CV=form_data['CV']
        )
    elif user_type == 'A':
        new_user = Alumni.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
            graduating_year=form_data['graduating_year'],
            dept=form_data['dept']
        )
    elif user_type == 'C':
        new_user = Company.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
            company_name=form_data['company_name'],
            desc=form_data['desc']
        )
    else:
        new_user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password1'],
            user_role=user_type,
            user_contact=user_data['user_contact'],
        )
    tag_names = user_data['tags']
    for tag_name in tag_names:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        new_user.tags.add(tag)

    return new_user

def index(request):
    return render(request, 'core/index.html')

def team(request):
    return render(request, 'core/team.html')

def dashboard(request):
    return render(request,'core/dashboard/company.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_role == 'S':
                    return redirect('dashboard_S')
                elif user.user_role == 'A':
                    return redirect('dashboard_A')
                elif user.user_role == 'C':
                    return redirect('dashboard_C')
                elif user.user_role == 'F':
                    admin_url = reverse('admin:index')
                    return redirect(admin_url)
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:index')

def signup1(request):
    if request.method == 'POST':
        userform = UserSignupForm(request.POST)
        if userform.is_valid():
            print("Hello")
            request.session['user_signup'] = userform.cleaned_data
            return redirect('core:signup2')
    else:
        userform = UserSignupForm()
    return render(request, 'core/signup/signup1_user.html', {'form': userform})

def signup2(request):
    if request.method == 'POST':
        userrole = RoleForm(request.POST)
        if userrole.is_valid():
            request.session['user_role'] = userrole.cleaned_data
            return redirect('core:signup3', user_type=request.session.get('user_role')['user_role'])
    else:
        userrole = RoleForm()
    return render(request, 'core/signup/signup2_role.html', {'form': userrole})

def signup3(request, user_type):

    user_data = request.session.get('user_signup')

    if user_type == 'A':
        template_name = 'core/signup/signup3_A.html'

        if request.method == 'POST':
            final_form = AlumniForm(request.POST)
            if final_form.is_valid():
                alumni_data = final_form.cleaned_data
                new_alumni = create_user(user_data=user_data, user_type=user_type, form_data=alumni_data)
                new_alumni.save()

                return redirect('core:index')
        else:
            final_form = AlumniForm()

    elif user_type == 'C':
        template_name = 'core/signup/signup3_C.html'

        if request.method == 'POST':
            final_form = CompanyForm(request.POST)
            if final_form.is_valid():
                company_data = final_form.cleaned_data
                new_company = create_user(user_data=user_data, user_type=user_type, form_data=company_data)
                new_company.save()

                return redirect('core:index')
        else:
            final_form = CompanyForm()
    
    elif user_type == 'S':
        template_name = 'core/signup/signup3_S.html'

        if request.method == 'POST':
            final_form = StudentForm(request.POST, request.FILES)
            if final_form.is_valid():
                student_data = final_form.cleaned_data
                new_student = create_user(user_data=user_data, user_type=user_type, form_data=student_data)
                new_student.save()

                return redirect('core:index')
        else:
            final_form = StudentForm()
    
    else:
        template_name=''
        final_form=''
        return redirect('core:index')
    
    return render(request, template_name, {'form': final_form})