from django.urls import path
from mainapp import views
from mainapp.apps import MainappConfig


app_name = MainappConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name="main_page"),
    path('contacts/', views.ContactsView.as_view(), name="contacts"),
    path('courses/', views.CoursesListView.as_view(), name="courses"),
    path('docsite/', views.DocSiteView.as_view(), name="docsite"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('news/', views.NewsView.as_view(), name="news"),
    path('news/<int:page>/', views.NewsWithPaginatorView.as_view(), name="news_paginator"),
    path('news/<int:pk>/detail', views.NewsDetailView.as_view(), name="news_detail"),
    path('news/create/', views.NewsCreateView.as_view(), name="news_create"),
    path('news/<int:pk>/update', views.NewsUpdateView.as_view(), name="news_update"),
    path('news/<int:pk>/delete', views.NewsDeleteView.as_view(), name="news_delete"),
    path('courses/<int:pk>/detail', views.CoursesDetailView.as_view(), name="courses_detail"),
    path('courses/feedback', views.CourseFeedbackFormProcessView.as_view(), name="course_feedback"),

]