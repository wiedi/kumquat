from django.urls import re_path
from cron import views

urlpatterns = [
	re_path(r'^job/$',                            views.CronjobList.as_view(),     name='cronjob_list'),
	re_path(r'^job/add$',                         views.CronjobCreate.as_view(),   name='cronjob_add'),
	re_path(r'^job/(?P<pk>\d+)/update$',          views.CronjobUpdate.as_view(),   name='cronjob_update'),
	re_path(r'^job/(?P<pk>\d+)/delete$',          views.CronjobDelete.as_view(),   name='cronjob_delete'),
]
