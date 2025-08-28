from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='getpost/main.html')),
    path('getform', views.getform, name='getform'),
    path('postform', views.postform, name='postform'),
    path('failform', views.failform, name='failform'),
    path('csrfform', views.csrfform, name='csrfform'),
    path('guess', views.guess, name='guess'),
]