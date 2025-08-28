from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='authz'
urlpatterns = [
    path('', TemplateView.as_view(template_name='authz/main.html')),
    path('manual', views.ManualProtect.as_view(), name='manual'),
    path('protect', views.ProtectView.as_view(), name='protect'),
]