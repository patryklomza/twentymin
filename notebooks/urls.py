from django.urls import path
from notebooks import views

urlpatterns = [
    path("new", views.new_note, name="new_note"),
    path("<int:notebook_id>/", views.view_notebook, name="view_notebook"),
    path("<int:notebook_id>/add_note", views.add_note, name="add_note"),
]
