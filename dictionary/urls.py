from django.urls import path, include
from dictionary import views

urlpatterns = [
   path(r'receive', views.receive, name="receive"),
   path(r'get', views.get, name="data_dictionary"),
   path('dataset/<model_name>/', views.dataset, name='dataset'),
]
