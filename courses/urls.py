from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='courses.index'),
    path('add/', views.add, name='courses.add'),
    path('check/', views.check, name='courses.check'),
    path('<int:id>/', views.list, name='courses.list'),
    path('video/<int:id>/', views.video, name='courses.video'),
    path('video/<int:video_id>/<str:new_time>/', views.update_time_view, name='courses.update_video_time')
]
