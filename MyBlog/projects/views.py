from django.shortcuts import render


def projects_view(request):
    return render(request, 'projects.html')