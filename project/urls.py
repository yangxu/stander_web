from django.urls import path, include
from project import views

urlpatterns = [
   path('<slug>/', views.project, name='project'),
]
