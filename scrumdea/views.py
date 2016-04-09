from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, FormView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from scrumdea import models as src_models
from scrumdea import forms as src_forms


# Create your views here.

def idea_list(request):
    if request.user.is_authenticated():
        queryset = src_models.GeneralIdea.objects.all()
        context = {
            "title": "authenticated User response",
            "idea_list": queryset
        }
    else:
        context = {
            "title": "access denied"
        }

    return render(request, "scrumdea/project/generalidea-list.html", context)


def create_general_idea(request):
    form = src_forms.GeneralIdeaForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.votes = 0
        instance.save()
    context = {
        "form" : form,

    }
    return render(request, "scrumdea/project/generalidea-create.html", context)


class Index(FormView):
    template_name = "scrumdea/project/login.html"
    form_class = AuthenticationForm


def sign_in_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/project/create/')
        else:
            # Return a 'disabled account' error message
            return HttpResponse('invalid login credentials entered')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse('invalid login credentials entered')


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


def generalidea_detail_view(request, pk):
    if request.user.is_authenticated():
        instance = get_object_or_404(src_models.GeneralIdea, id=pk)
        context = {
            "title": "authenticated User response",
            "instance": instance
        }
    else:
        context = {
            "title": "access denied (not authenticated)"
        }

    return render(request, "scrumdea/project/generalidea-detail.html", context)
