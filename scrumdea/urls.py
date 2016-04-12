from django.conf.urls import url

from . import views

urlpatterns = [
    # General idea
    url(r'^$', views.idea_list, name='idea_list'),
    url(r'^general-ideas/(?P<pk>\d+)/$', views.generalidea_detail_view, name='general_idea_detail_view'),
    url(r'^general-ideas/create/$', views.create_general_idea, name='create_general_idea'),
    url(r'^general-ideas/(?P<pk>\d+)/edit$', views.edit_general_idea, name='general_idea_edit_view'),
    url(r'^general-ideas/(?P<pk>\d+)/delete$', views.delete_general_idea, name='general_idea_delete_view'),

    # Project
    url(r'^projects/$', views.ProjectList.as_view(), name='project_list'),



    url(r'^(?P<project_id>[0-9]+)/$', views.project, name='project'),
    url(r'^project/view/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='detailProject_view'),
    url(r'^project/create/$', views.ProjectCreateView.as_view(), name='createProject_view'),
    url(r'^project/create/save/$', views.get_name, name='createProjectSubmit_function_view'),

]
