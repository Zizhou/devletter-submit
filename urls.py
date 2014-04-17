from django.conf.urls import patterns, url

from submit import views

urlpatterns = patterns('',
    url(r'^$', views.main_page, name = 'main'),
    url(r'send', views.send, name = 'send'),

)
