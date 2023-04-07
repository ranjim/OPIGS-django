from django.shortcuts import render, redirect
from .forms import SignupForm

def index(request):
    return render(request, 'core/index.html')

def team(request):
    return render(request, 'core/team.html')

def signup1(request):
    if request.method == 'POST':
        return redirect('core:signup2')
    return render(request, 'core/signup/signup1_user.html')

def signup2(request):
    if request.method == 'POST':
        user_role = request.POST.get('user_role')
        print("userroel:", user_role)
        return redirect('core:signup3', user_type=user_role)
    return render(request, 'core/signup/signup2_role.html')

def signup3(request, user_type):
    if user_type == 'A':
        template_name = 'core/signup/signup3_A.html'
    elif user_type == 'C':
        template_name = 'core/signup/signup3_C.html'
    elif user_type == 'S':
        template_name = 'core/signup/signup3_S.html'
    
    return render(request, template_name)