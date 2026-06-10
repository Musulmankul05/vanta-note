from django.urls import path

from notes import views

urlpatterns = [
    path('', views.note_list_view, name='note-menu'),
    path('note/<int:pk>', views.note_detail_view, name='note-detail'),
    path('entry/<int:pk>', views.note_burning_view, name='note-burning'),
    path('create/', views.note_create_view, name='note-create'),
    path('edit/<int:pk>/', views.note_edit_view, name='note-edit'),
    path('delete/<int:pk>/', views.note_delete_view, name='note-delete'),
    path('api/v1/notes', views.NoteListCreateView.as_view())
]