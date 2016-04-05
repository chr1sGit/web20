

from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.shortcuts import render

from scrumdea import models as src_models
from scrumdea import forms as src_forms

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the SCRUMdea index.")


def project(request, project_id):
    response = "You're looking at project %s."
    return HttpResponse(response % project_id)

class ProjectDetailView(DetailView):
    model = src_models.Project
    template_name = 'scrumdea/project/detail.html'
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    model = src_models.Project
    template_name = 'scrumdea/project/create-update.html'
    context_object_name = 'project'
    form_class = src_forms.ProjectFrom
