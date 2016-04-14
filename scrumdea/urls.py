from django.conf.urls import url, handler404
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # General idea
    url(r'^$', views.GeneralIdeaListView.as_view(), name='idea_list'),
    url(r'^general-ideas/(?P<pk>\d+)/$', login_required(views.GeneralIdeaDetailView.as_view()), name='general_idea_detail_view'),
    url(r'^general-ideas/create/$', views.create_general_idea, name='create_general_idea_view'),
    url(r'^general-ideas/(?P<pk>\d+)/edit$', views.edit_general_idea, name='general_idea_edit_view'),
    url(r'^general-ideas/(?P<pk>\d+)/delete$', views.delete_general_idea, name='general_idea_delete_view'),

    # Projects
    url(r'^projects/$', views.ProjectNewListView.as_view(), name='project_list_view'),
    url(r'^projects/create$', views.ProjectCreateView.as_view(), name='project_create_view'),
    url(r'^projects/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project_detail_view'),



    # old URLs
    url(r'^(?P<project_id>[0-9]+)/$', views.project, name='project'),
    url(r'^project/view/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='detailProject_view'),
    url(r'^project/create/$', views.ProjectCreateView.as_view(), name='createProject_view'),
    url(r'^project/create/save/$', views.get_name, name='createProjectSubmit_function_view'),

]

handler404 = 'views.page_not_found'
