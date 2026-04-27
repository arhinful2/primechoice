from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('admissions/', views.admissions, name='admissions'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('api/track-click/', views.track_click, name='track_click'),
]