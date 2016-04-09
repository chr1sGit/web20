from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.idea_list, name='idea_list'),
    url(r'^general-ideas/(?P<pk>\d+)/$', views.generalidea_detail_view, name='generalideadetailview'),
    url(r'^general-ideas/create/$', views.create_general_idea, name='creategeneralidea'),

    url(r'^(?P<project_id>[0-9]+)/$', views.project, name='project'),
    url(r'^project/view/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='detailProject_view'),
    url(r'^project/create/$', views.ProjectCreateView.as_view(), name='createProject_view'),
    url(r'^project/create/save/$', views.get_name, name='createProjectSubmit_function_view'),

]
