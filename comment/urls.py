from django.urls import path
from . import views


urlpatterns = [
    path('comment_update', views.comment_update, name='comment_update'),
]
