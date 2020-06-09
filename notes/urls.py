from django.urls import path
from notes import views

urlpatterns = [
    path("new", views.new_note, name="new_note"),
    path("books/<int:book_id>/", views.view_note, name="view_note"),
    path("books/<int:book_id>/add_note", views.add_note, name="add_note"),
]
