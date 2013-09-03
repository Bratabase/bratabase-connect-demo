from django.contrib.auth.views import logout
from django.conf.urls import patterns, include, url

from website.views import home


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^logout/$',
        logout,
        {'template_name': 'logout.html'},
        name='auth_logout'),
    url(r'^', include('social_auth.urls')),
)
