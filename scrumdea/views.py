from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, FormView, View, ListView, DeleteView, \
    RedirectView
from django.shortcuts import render, get_object_or_404, render_to_response, resolve_url, redirect
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib import parse as urlparse
from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.contrib import auth
from scrumdea.utils import default_redirect

from scrumdea import models as src_models
from scrumdea import forms as src_forms


# General Idea Views
class GeneralIdeaListView(LoginRequiredMixin, ListView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/general-idea/generalidea-list.html"


class GeneralIdeaDetailView(LoginRequiredMixin, DetailView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/general-idea/generalidea-detail.html"


class GeneralIdeaCreateView(LoginRequiredMixin, CreateView):
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


class GeneralIdeaUpdateView(LoginRequiredMixin, UpdateView):
    model = src_models.GeneralIdea
    fields = ['title', 'description']
    template_name = "scrumdea/general-idea/login.html"

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


class GeneralIdeaDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.GeneralIdea
    template_name = "scrumdea/general-idea/generalidea-delete.html"

    def get_success_url(self):
        return reverse('general_idea_list_view')


# Project Views
class ProjectNewListView(LoginRequiredMixin, ListView):
    model = src_models.Project
    template_name = "scrumdea/project/project-list.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = src_models.Project
    template_name = 'scrumdea/project/project-detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['sprints'] = src_models.Sprint.objects.filter(project=self.kwargs['pk'])
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
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


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.Project
    template_name = "scrumdea/project/project-delete.html"

    def get_success_url(self):
        return reverse('project_list_view')


class ProjectEditView(LoginRequiredMixin, UpdateView):
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


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = src_models.Project
    template_name = 'scrumdea/project/project-create.html'
    context_object_name = 'project'
    form_class = src_forms.ProjectForm


# sprint views
class SprintListView(LoginRequiredMixin, ListView):
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


class SprintCreateView(LoginRequiredMixin, CreateView):
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


class SprintDetailView(LoginRequiredMixin, DetailView):
    model = src_models.Sprint
    template_name = 'scrumdea/sprint/sprint-detail.html'

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_context_data(self, **kwargs):
        context = super(SprintDetailView, self).get_context_data(**kwargs)
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
        context['sprint_complete_in_percent'] = round(percent_complete, 1)
        return context


class SprintDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.Sprint
    template_name = "scrumdea/sprint/sprint-delete.html"

    def get_object(self, queryset=None):
        return src_models.Sprint.objects.get(id=self.kwargs['spk'])

    def get_success_url(self):
        return reverse('sprint_list_view',
                       kwargs={'pk': (src_models.Sprint.objects.get(id=self.kwargs['spk'])).project.id})


class SprintEditView(LoginRequiredMixin, UpdateView):
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
class TaskListView(LoginRequiredMixin, ListView):
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


class TaskCreateView(LoginRequiredMixin, CreateView):
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


class TaskDetailView(LoginRequiredMixin, DetailView):
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


class TaskEditView(LoginRequiredMixin, UpdateView):
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


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = src_models.Task
    template_name = "scrumdea/task/task-delete.html"

    def get_object(self, queryset=None):
        return src_models.Task.objects.get(id=self.kwargs['tpk'])

    def get_success_url(self):
        return reverse('sprint_detail_view', kwargs={'pk': self.kwargs['pk'], 'spk': self.kwargs['spk']})


class TaskMoveRight(LoginRequiredMixin, RedirectView):
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


# authentication

class LoginView(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'scrumdea/authentication/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can check the test cookie stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, ''))

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(TemplateResponseMixin, View):
    template_name = "scrumdea/authentication/logout.html"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = kwargs
        redirect_field_name = self.get_redirect_field_name()
        redirect_field_value = self.request.POST.get(
            redirect_field_name, self.request.GET.get(redirect_field_name, ''))
        context.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": redirect_field_value,
        })
        return context

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


# vote view
class VoteView(View):
    def post(self, request, *args, **kwargs):
        # - retrieve the user_profile
        # - retrieve the suggestedName he voted for
        # - query the votes to see if this combination of user_profile + suggestedName already exists


        user = self.request.user
        generalIdea = None
        inProjectIdea = None

        vote, created = src_models.Vote.objects.get_or_create(
            user=user,
            generalIdea=generalIdea,
            inProjectIdea=inProjectIdea
        )

        # get_or_create will return a tuple
        # where created is True if the method created the Vote
        # False if there was a vote for this user and this name already
        # You now want to use the value from 'created'
        # to decide wether the vote is valid or not

        if not created:
            return HttpResponse('You already voted for this.')
        else:
            return HttpResponse('Awesome, thanks for voting!')


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
