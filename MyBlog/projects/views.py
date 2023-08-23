from django.shortcuts import render
from .models import Projects


def projects_view(request):
    projects = Projects.objects.order_by('-posted_date')
    
    output = {
        'projects' : projects
    }
    
    return render(request, 'projects/projects.html', output)