# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'resume.core.views.home', name='home'),
    url(r'^articles/$', 'resume.core.views.all_articles', name='all_articles'),
    url(r'^article/(?P<slug>[-\w]+)/$', 'resume.core.views.article', name='article'),
    url(r'^write/$', 'resume.core.views.write', name='write'),
    url(r'^admin/', include(admin.site.urls)),
)
