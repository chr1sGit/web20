from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<project_id>[0-9]+)/$', views.project, name='project'),
    url(r'^project/view/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='detailProject_view'),
    url(r'^project/create/$', views.ProjectCreateView.as_view(), name='createProject_view'),
    url(r'^project/create/save/$', views.get_name, name='createProjectSubmit_function_view')
]
