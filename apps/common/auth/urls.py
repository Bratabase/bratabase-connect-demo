# coding: utf-8

from django.conf.urls import patterns, url

from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
    url(r'^logout/',
        auth_views.logout,
        {'template_name': 'auth/logout.html'},
        name='auth_logout'),
)
