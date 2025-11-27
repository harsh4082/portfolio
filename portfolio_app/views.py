from django.shortcuts import render
from .models import Project, Education, ContactInfo

def home(request):
    projects = Project.objects.all().order_by('-id')
    education = Education.objects.all().order_by('-id')
    contact = ContactInfo.objects.first()
    return render(request, 'home.html', {'projects': projects, 'education': education, 'contact': contact})

def about(request):
    projects = Project.objects.all().order_by('-id')
    education = Education.objects.all().order_by('-id')
    contact = ContactInfo.objects.first()
    return render(request, 'about.html', {'projects': projects, 'education': education, 'contact': contact})


from django.shortcuts import render
from .models import Project, Education, ContactInfo, Skill

def home(request):
    projects = Project.objects.all().order_by('-id')
    education = Education.objects.all().order_by('-id')
    contact = ContactInfo.objects.first()
    skills = Skill.objects.all()
    return render(request, 'home.html', {
        'projects': projects,
        'education': education,
        'contact': contact,
        'skills': skills,
    })

def about(request):
    projects = Project.objects.all().order_by('-id')
    education = Education.objects.all().order_by('-id')
    contact = ContactInfo.objects.first()
    skills = Skill.objects.all()
    return render(request, 'about.html', {
        'projects': projects,
        'education': education,
        'contact': contact,
        'skills': skills,
    })


