from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
  url(r'^domains/$',                   views.DomainList.as_view(),   name='domain_list'),
  url(r'^domains/add$',                views.DomainCreate.as_view(), name='domain_add'),
  url(r'^domains/(?P<pk>\d+)/delete$', views.DomainDelete.as_view(), name='domain_delete'),
)