from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, FormView, View, ListView, DeleteView
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse

from scrumdea import models as src_models
from scrumdea import forms as src_forms


# General Idea Views
class GeneralIdeaListView(ListView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/general-idea/generalidea-list.html"


class GeneralIdeaDetailView(DetailView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/general-idea/generalidea-detail.html"


class GeneralIdeaCreateView(CreateView):
    model = src_models.GeneralIdea
    fields = ['title', 'description']
    template_name = "scrumdea/general-idea/generalidea-create.html"

    def get_success_url(self):
        return reverse('general_idea_detail_view', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> New Idea created :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class GeneralIdeaUpdateView(UpdateView):
    model = src_models.GeneralIdea
    fields = ['title', 'description']
    template_name = "scrumdea/general-idea/generalidea-update.html"

    def get_success_url(self):
        return reverse('general_idea_detail_view', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Idea updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class GeneralIdeaDeleteView(DeleteView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/general-idea/generalidea-delete.html"

    def get_success_url(self):
        return reverse('general_idea_list_view')


# Project Views
class ProjectNewListView(ListView):
    model = src_models.Project
    template_name = "scrumdea/project/project-list.html"


class ProjectDetailView(DetailView):
    model = src_models.Project
    template_name = 'scrumdea/project/project-detail.html'


class ProjectCreateView(CreateView):
    model = src_models.Project
    fields = ['name', 'description']
    template_name = "scrumdea/project/project-create.html"

    def get_success_url(self):
        return reverse("project_detail_view", args=self.object.id)

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> New project created :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class ProjectCreateView2(View):
    def get(self, request):
        if request.user.is_authenticated():
            form = src_forms.GeneralIdeaForm()
            context = {
                "form": form,
            }
            return render(request, "scrumdea/project/project-create.html", context)
        else:
            return

    def post(self, request):
        if request.user.is_authenticated():
            form = src_forms.GeneralIdeaForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                # success
                messages.success(request, "<b>Success!</b> New Project created :)",
                                 extra_tags='alert alert-success safe')
                return HttpResponseRedirect('/projects/' + str(instance.id))
            else:
                messages.error(request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                               extra_tags='alert alert-danger safe')
            context = {
                "form": form,
            }
            return render(request, "scrumdea/project/generalidea-create.html", context)
        else:
            messages.error(request, "<b>Not signed in</b> Please authenticate!")
            return HttpResponseRedirect('/projects/')





class ProjectCreateView(CreateView):
    model = src_models.Project
    template_name = 'scrumdea/project/project-create.html'
    context_object_name = 'project'
    form_class = src_forms.ProjectForm


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


def page_not_found(request):
    response = render_to_response('scrumdea/404.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response
