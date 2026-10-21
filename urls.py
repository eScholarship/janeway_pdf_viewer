from django.urls import re_path

from plugins.pdf_viewer import views


urlpatterns = [
    re_path(r'^manager/$', views.manager, name='pdf_viewer_manager'),
]
