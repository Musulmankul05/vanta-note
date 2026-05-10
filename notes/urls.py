from django.urls import path

from notes import views

urlpatterns = [
    path('', views.note_list_view, name='note-menu'),
    path('note/<int:pk>', views.note_detail_view, name='note-detail'),
]