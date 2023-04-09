from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .forms import *
from .models import Application
from .utils import create_user
from taggit.models import Tag

def index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return render(request, 'core/index.html', {'form': form})

def team(request):
    return render(request, 'core/team.html')

def success(request):
    return render(request, 'core/signup/success.html')

@login_required
def dashboard_S(request):
    user = Student.objects.filter(username=request.user.username)[0]

    all_chats = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    recent_chats = []
    others = []
    for chat in all_chats:
        if chat.sender == request.user and chat.receiver not in others:
            recent_chats.append(chat)
            others.append(chat.receiver)
        elif chat.receiver == request.user and chat.sender not in others:
            recent_chats.append(chat)
            others.append(chat.sender)

    notifications = Notification.objects.all().order_by('posted_on')

    return render(request, 'core/dashboard/dashboard_S.html', {
        'user': user,
        'recent_chats': recent_chats,
        'notifications': notifications
    })

@login_required
def dashboard_A(request):
    user = Alumni.objects.filter(username=request.user.username)[0]

    all_chats = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    recent_chats = []
    others = []
    for chat in all_chats:
        if chat.sender == request.user and chat.receiver not in others:
            recent_chats.append(chat)
            others.append(chat.receiver)
        elif chat.receiver == request.user and chat.sender not in others:
            recent_chats.append(chat)
            others.append(chat.sender)

    notifications = Notification.objects.all().order_by('posted_on')

    return render(request, 'core/dashboard/dashboard_A.html', {
        'user': user,
        'recent_chats': recent_chats,
        'notifications': notifications
    })

@login_required
def dashboard_C(request):
    user = Company.objects.filter(username=request.user.username)[0]
    applications = Application.objects.filter(Q(recruiter=request.user) & Q(is_shortlisted=False))
    shortlists = Application.objects.filter(Q(recruiter=request.user) & Q(is_shortlisted=True))
    notifications = Notification.objects.all()

    return render(request, 'core/dashboard/dashboard_C.html', {
        'user': user,
        'applications': applications,
        'shortlists': shortlists,
        'notifications': notifications
    })

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
                    return redirect('core:dashboard_S')
                elif user.user_role == 'A':
                    return redirect('core:dashboard_A')
                elif user.user_role == 'C':
                    return redirect('core:dashboard_C')
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

                return redirect('core:success')
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

                return redirect('core:success')
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

                return redirect('core:success')
        else:
            final_form = StudentForm()
    
    else:
        template_name=''
        final_form=''
        return redirect('core:index')
    
    return render(request, template_name, {'form': final_form})

def chat_view(request, username):
    sender = request.user
    receiver = User.objects.filter(username=username)[0]
    chat_history = Chat.objects.filter(Q(sender=sender) & Q(receiver=receiver) | Q(sender=receiver) & Q(receiver=sender))
    return render(request, 'core/chat.html', {'sender': sender, 'receiver': receiver, 'chat_history': chat_history})

def send_chat(request, username):
    if request.method == "POST":
        sender = request.user
        message = request.POST.get('message')
        receiver = User.objects.filter(username=username)[0]
        
        Chat.objects.create(sender=sender, receiver=receiver, message=message)
        return redirect('core:chat', username=username)

def search_results(request):

    student = Student.objects.filter(username=request.user.username)[0]

    query = request.GET.get('query')
    try:
        users = User.objects.filter(tags__name__in=query.split())
    except Tag.DoesNotExist:
        users = []

    companies = []
    alumnis = []
    students = []
    application = Application.objects.filter(applicant=student)
    if len(application) == 0:
        applied = False
    else:
        applied = True
    
    for user in users:
        if user.user_role == 'C':
            companies.append(Company.objects.filter(username=user.username)[0])
        elif user.user_role == 'A':
            alumnis.append(user)
        elif user.user_role == 'S':
            students.append(user)

    return render(request, 'core/search_results.html', {
        'companies': companies,
        'alumnis': alumnis,
        'students': students,
        'applied': applied
    })

@login_required
def edit_profile(request):
    user_profile = request.user

    if user_profile.user_role == 'S':
        page = 'core:dashboard_S'
    elif user_profile.user_role == 'A':
        page = 'core:dashboard_A'
    else:
        page = 'core:dashboard_C'

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect(page)
    else:
        form = EditUserForm(instance=user_profile)
    return render(request, 'core/dashboard/edit_profile.html', {'editform': form})

def create_application(request, username):
    if request.method == 'POST':
        # Get data from 
        recruiter = Company.objects.filter(username=username)[0]
        applicant = Student.objects.filter(username=request.user)[0]
        
        # Create application instance
        Application.objects.create(
            recruiter=recruiter,
            applicant=applicant,
            is_shortlisted=False
        )
        
        # Redirect to a success page
        return redirect('core:dashboard_S')

def remove_application(request, username):
    if request.method == 'POST':
        # Get data from 
        recruiter = Company.objects.filter(username=request.user.username)[0]
        applicant = Student.objects.filter(username=username)[0]
        
        # Create application instance
        application = Application.objects.filter(applicant=applicant)
        application.delete()
        
        # Redirect to a success page
        return redirect('core:dashboard_C')

def shortlist_application(request, username):
    if request.method == 'POST':
        # Get data from 
        recruiter = Company.objects.filter(username=request.user.username)[0]
        applicant = Student.objects.filter(username=username)[0]
        
        # Create application instance
        application = Application.objects.get(applicant=applicant)

        # update the values of the application object
        application.is_shortlisted = True
        application.save()
        
        # Redirect to a success page
        return redirect('core:dashboard_C')