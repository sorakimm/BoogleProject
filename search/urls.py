from django.conf.urls import url
from . import views
#from . import search_views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': r'C:\Users\bit\Boogle\search\images'}),
    url(r'^search/(?P<mode>[a-z]+)/(?P<keyword>[\w|\W]+)/Page(?P<page>\d+)/$', views.SearchPage),
    url(r'^search/(?P<mode>[a-z]+)/(?P<keyword>[\w|\W]+)/$', views.SearchPage),
   
    
]