from django.contrib import admin
from .models import Projects, Technology
from .forms import ProjectsAdminForm


class ProjectsAdmin(admin.ModelAdmin):
    form = ProjectsAdminForm
    list_display = ['project_url', 'description', 'status', 'likes', 'dislikes']
    filter_horizontal = ['technologies']

admin.site.register(Projects, ProjectsAdmin)

class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name']  

admin.site.register(Technology, TechnologyAdmin)