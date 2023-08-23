from django import forms
from .models import Projects

class ProjectsAdminForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['project_url', 'description', 'status', 'likes', 'dislikes', 'technologies']
