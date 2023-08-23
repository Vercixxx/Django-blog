from django.shortcuts import render
from .models import Projects

from bs4 import BeautifulSoup
import requests


def projects_view(request):
   
    projects = get_projects(request)
    
    output = {
        'projects' : projects,
    }
    
    return render(request, 'projects/projects.html', output)

def get_projects(request):
    all_projects = Projects.objects.order_by('-posted_date')
    
    for project in all_projects:
        # Get info from github
        url = project.project_url
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        
        
        
        
        # Project title and decription
        
        page_title = soup.title.string
        
        parts = page_title.split('/')
        if len(parts) > 1:
            title = parts[1].split(':')[0].strip()  # Część między / a :
            if ':' in parts[1]:
                desc = parts[1].split(':')[1].strip()  # Część po :
            else:
                desc = 'No description yet'
        else:
            title = ''
            desc = ''
            
        project.title = title
        project.description = desc
        
        # Commits number
        spans = soup.find_all('span', class_='d-none d-sm-inline')
        for span in spans:
            for tag in span.contents:
                if tag.name=="strong" :
                    project.commits = tag.get_text()
                    
        a_tags = soup.find_all('a', class_='ml-3 Link--primary no-underline')
        for a_tag in a_tags:
            strong_tag = a_tag.find('strong')
            if strong_tag:
                project.branches = strong_tag.get_text()
                break
                    
                    
                    
                    
        project.save()
    

    return all_projects