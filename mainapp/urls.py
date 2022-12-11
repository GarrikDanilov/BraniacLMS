from django.urls import path
from django.views.decorators.cache import cache_page
from mainapp import views
from mainapp.apps import MainappConfig


app_name = MainappConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name="main_page"),
    path('contacts/', views.ContactsView.as_view(), name="contacts"),
    path('docsite/', views.DocSiteView.as_view(), name="docsite"),
    path('login/', views.LoginView.as_view(), name="login"),
    # News
    path('news/', views.NewsView.as_view(), name="news"),
    path('news/<int:page>/', views.NewsWithPaginatorView.as_view(), name="news_paginator"),
    path('news/<int:pk>/detail', views.NewsDetailView.as_view(), name="news_detail"),
    path('news/create/', views.NewsCreateView.as_view(), name="news_create"),
    path('news/<int:pk>/update', views.NewsUpdateView.as_view(), name="news_update"),
    path('news/<int:pk>/delete', views.NewsDeleteView.as_view(), name="news_delete"),
    # Courses
    path('courses/', cache_page(300)(views.CoursesListView.as_view()), name="courses"),
    path('courses/<int:pk>/detail', views.CoursesDetailView.as_view(), name="courses_detail"),
    path('courses/feedback', views.CourseFeedbackFormProcessView.as_view(), name="course_feedback"),
    # Logs
    path('logs/', views.LogView.as_view(), name='logs_list'),
    path('logs_download/', views.LogDownloadView.as_view(), name='logs_download'),
]
