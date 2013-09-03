from django.conf.urls import patterns, include, url

from website.views import home


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^', include('social_auth.urls')),
    url(r'^', include('common.auth.urls')),
)
