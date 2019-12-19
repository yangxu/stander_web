from django.shortcuts import render
from django.shortcuts import get_object_or_404
from project.models import Project

def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    if project.template_name:
       template_name = project.template_name
    else:
       template_name = 'flatpages/default.html'
    
    filepage = {
                 "title": project.title,
                 "content": project.description,
                 "project": project,
               }
    return render(request, template_name, filepage)
