from django.urls import path, include
from portal import views

urlpatterns = [
        path('file_page/<path:slug>/', views.filepage, name='file_page'),
        path('template/<template_id>/edit/', views.edit_template, name='edit_template'),
        path('flatpage/<flatpage_id>/edit/', views.edit_flatpage, name='edit_flatpage'),
        path('flatpage_header/<flatpage_id>/edit/', views.edit_flatpage_header, name='edit_flatpage_header'),
]
