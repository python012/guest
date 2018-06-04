from django.conf.urls import url
from sign import views_if


urlpatterns = [
    #sign system interface:
    #ex : /api/add_event/
    url(r'^index/$', views_if.add_event, name='add_event'),
]