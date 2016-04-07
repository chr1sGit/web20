from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
    form_class = src_forms.ProjectForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = src_forms.ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = src_forms.ProjectForm()

    return render(request, 'name.html', {'form': form})
