from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, FormView, View, ListView, DeleteView, RedirectView
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sprints'] = src_models.Sprint.objects.filter(project=self.kwargs['pk'])
        return context


class ProjectCreateView(CreateView):
    model = src_models.Project
    fields = ['name', 'description']
    template_name = "scrumdea/project/project-create.html"

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> New Idea created :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_absolute_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class ProjectDeleteView(DeleteView):
    model = src_models.Project
    template_name = "scrumdea/project/project-delete.html"

    def get_success_url(self):
        return reverse('project_list_view')


class ProjectEditView(UpdateView):
    model = src_models.Project
    fields = ['name', 'description']
    template_name = "scrumdea/project/project-update.html"

    def get_success_url(self):
        return reverse('project_detail_view', args=(self.object.id,))

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Idea updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class ProjectCreateView(CreateView):
    model = src_models.Project
    template_name = 'scrumdea/project/project-create.html'
    context_object_name = 'project'
    form_class = src_forms.ProjectForm


# sprint views
class SprintListView(ListView):
    model = src_models.Sprint
    template_name = "scrumdea/sprint/sprint-list.html"

    def get_queryset(self):
        return src_models.Sprint.objects.filter(project=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SprintListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project'] = src_models.Project.objects.get(id=self.kwargs['pk'])
        return context


class SprintCreateView(CreateView):
    model = src_models.Sprint
    template_name = 'scrumdea/sprint/sprint-create.html'
    context_object_name = 'sprint'
    form_class = src_forms.SprintForm

    def get_success_url(self):
        return reverse('sprint_list_view', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Sprint created! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.project = src_models.Project.objects.get(id=self.kwargs['pk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class SprintDetailView(DetailView):
    model = src_models.Sprint
    template_name = 'scrumdea/sprint/sprint-detail.html'

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SprintDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tasks_todo'] = src_models.Task.objects.filter(sprint=self.kwargs['spk'], phase='ToDo')
        context['tasks_in_progress'] = src_models.Task.objects.filter(sprint=self.kwargs['spk'], phase='iP')
        context['tasks_in_review'] = src_models.Task.objects.filter(sprint=self.kwargs['spk'], phase='iR')
        context['tasks_finished'] = src_models.Task.objects.filter(sprint=self.kwargs['spk'], phase='F')
        context['project'] = src_models.Project.objects.get(id=self.kwargs['pk'])
        context['sprint'] = src_models.Sprint.objects.get(id=self.kwargs['spk'])
        percent_complete = 0
        tasks_count = src_models.Task.objects.filter(sprint=self.kwargs['spk']).count()
        tasks_finished = src_models.Task.objects.filter(sprint=self.kwargs['spk'], phase='F').count()
        if tasks_count != 0:
            percent_complete = (tasks_finished / tasks_count) * 100
        #percent_complete = round(((src_models.Task.objects.filter(sprint=self.kwargs['spk'], phase='F').count() / src_models.Task.objects.filter(sprint=self.kwargs['spk']).count()) * 100), 1)
        context['sprint_complete_in_percent'] = round(percent_complete, 1)
        return context


class SprintDeleteView(DeleteView):
    model = src_models.Sprint
    template_name = "scrumdea/sprint/sprint-delete.html"

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_success_url(self):
        return reverse('sprint_list_view',
                       kwargs={'pk': (src_models.Sprint.objects.get(id=self.kwargs['spk'])).project.id})


class SprintEditView(UpdateView):
    model = src_models.Sprint
    fields = ['name', ]
    template_name = "scrumdea/sprint/task-update.html"

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_success_url(self):
        return reverse('sprint_detail_view',
                       kwargs={'pk': self.kwargs['pk'],
                               'spk': self.kwargs['spk']
                               })

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Sprint updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


# task view
class TaskListView(ListView):
    model = src_models.Task
    template_name = "scrumdea/task/task-list.html"

    def get_queryset(self):
        return src_models.Task.objects.filter(sprint=self.kwargs['spk'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TaskListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project'] = src_models.Project.objects.get(id=self.kwargs['pk'])
        context['sprint'] = src_models.Sprint.objects.get(id=self.kwargs['spk'])
        return context


class TaskCreateView(CreateView):
    model = src_models.Task
    template_name = 'scrumdea/task/task-create.html'
    context_object_name = 'task'
    form_class = src_forms.TaskForm

    def get_success_url(self):
        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': self.kwargs['spk']})

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Task created! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.sprint = src_models.Sprint.objects.get(id=self.kwargs['spk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class TaskDetailView(DetailView):
    model = src_models.Task
    template_name = 'scrumdea/task/task-detail.html'

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project'] = src_models.Project.objects.get(id=self.kwargs['pk'])
        return context


class TaskEditView(UpdateView):
    model = src_models.Task
    form_class = src_forms.TaskForm
    template_name = "scrumdea/task/task-update.html"

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def get_success_url(self):
        return reverse('sprint_detail_view',
                       kwargs={'pk': self.kwargs['pk'],
                               'spk': self.kwargs['spk']
                               })

    def form_valid(self, form):
        messages.success(self.request, "<b>Success!</b> Task updated! :)", extra_tags='alert alert-success safe')
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "<b>Oh Snap!</b> Something went wrong. Check your input.",
                       extra_tags='alert alert-danger safe')
        return self.render_to_response(self.get_context_data())


class TaskDeleteView(DeleteView):
    model = src_models.Task
    template_name = "scrumdea/task/task-delete.html"

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def get_success_url(self):
        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': self.kwargs['spk']})


class TaskMoveRight(RedirectView):
    model = src_models.Task

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def new_phase(self, argument):
        switcher = {
            'ToDo': 'iP',
            'iP': 'iR',
            'iR': 'F',
        }
        return switcher.get(argument, "F")

    def get_redirect_url(self, *args, **kwargs):

        task = src_models.Task.objects.get(id=self.kwargs['tpk'])
        task.phase = self.new_phase(task.phase)
        task.save()

        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': self.kwargs['spk']})




# trash
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
