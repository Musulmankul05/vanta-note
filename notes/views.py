import markdown
from django.shortcuts import render, get_object_or_404
from .models import Note

# Create your views here.
def note_list_view(request):
    notes = Note.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'note-list.html', context={'notes': notes, 'user': request.user})

def note_detail_view(request, pk):
    md = markdown.Markdown(extensions=['fenced_code'])
    note = get_object_or_404(Note, pk=pk)
    note.content = md.convert(note.content)


    if request.headers.get("HX-Request"):
        return render(request, 'note-detail.html', context={'note': note})

    return render(request, 'note-list.html', context={'note': note})