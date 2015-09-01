from django.conf.urls import patterns, url

from submit import views

urlpatterns = patterns('',
    url(r'^$', views.main_page, name = 'main'),
    url(r'^send$', views.send, name = 'send'),
    url(r'^missing/$', views.MissingView.as_view(), name = 'missing'),
    url(r'^tweet/$', views.tweet, name = 'tweet'),
    url(r'^tweet_lookup/(?P<game_id>.*)$', views.tweet_lookup, name = 'tweet_lookup'), 
    #FUCKING regex
    url(r'^name_lookup/(?P<name>.*)$', views.name_lookup, name = 'lookup'), 
    url(r'^dev_lookup/(?P<name>.*)$', views.dev_lookup, name = 'dlookup'), 
)
