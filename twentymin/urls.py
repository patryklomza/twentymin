"""twentymin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from notes import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("notes/new", views.new_note, name="new_note"),
    path("notes/books/<int:book_id>/", views.view_note, name="view_note"),
    path("notes/books/<int:book_id>/add_note", views.add_note, name="add_note"),
]
