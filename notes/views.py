from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404
from .serializers import NoteSerializer
from .models import Note
import markdown

# Create your views here.
def note_list_view(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user).order_by('-created_at')
        return render(request, 'note-list.html', context={'notes': notes, 'user': request.user})
    return render(request, 'note-list.html')

def note_detail_view(request, pk):

    # master_key = request.session.get('master_key')
    #
    # if not master_key:
    #     from django.contrib.auth import logout
    #     logout(request)
    #     return redirect('login')
    note = get_object_or_404(Note, pk=pk)
    #
    # try:
    #     decrypted = note.decrypt_note_via_password(master_key)
    # except Exception as e:
    #     decrypted = 'Error: failed to decrypt'

    if note.is_expired:
        note.delete()
        return render(request, '404.html', {'message': 'Protocol Error: Entry Expired'})

    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'sane_lists'])

    note.content = md.convert(note.content)
    if request.headers.get("HX-Request"):
        return render(request, 'note-detail.html', context={'note': note})
    
    if note.is_burn_after_reading:
        note.delete()

    return render(request, 'note-list.html', context={'note': note})

def note_burning_view(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if not note.is_burn_after_reading:
        raise Http404
    title = note.title
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'sane_lists'])
    content = md.convert(note.content)
    created_date = note.created_at
    note.delete()
    return render(request, 'note-burning.html', context={'title': title, 'content': content, 'created_date': created_date})


@login_required
def note_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        lifetime = request.POST.get('lifetime')

        note = Note(title=title, content=content, author=request.user)
        match lifetime:
            case '1h':
                note.expires_at = timezone.now() + timedelta(hours=1)
            case '24h':
                note.expires_at = timezone.now() + timedelta(hours=24)
            case '7d':
                note.expires_at = timezone.now() + timedelta(days=7)

        note.is_burn_after_reading = 'burn_after_reading' in request.POST
        master_key = request.session.get('master_key')

        note.save(master_key=master_key)

        return redirect('note-menu')
    return render(request, 'note-create.html')

@login_required
def note_delete_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('note-menu')


@login_required
def note_edit_view(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    master_key = request.session.get('master_key')


    if request.method == "POST":
        note.title = request.POST.get("title")
        note.content = request.POST.get('content')
        note.save(master_key=master_key)
        return redirect('note-menu')

    return render(request, 'note-create.html', {
        'note': note,
        'is_edit': True
    })


# API ----------------

class NoteListCreateView(ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
