from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def team(request):
    return render(request, 'core/team.html')

def register(request):
    user_types = ["Student", "Alumnus", "Company Admin"]
    return render(request, 'core/register.html', {'user_types': user_types})