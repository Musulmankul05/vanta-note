from datetime import timedelta
from django.utils import timezone
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from django.contrib.auth.decorators import login_required

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

@login_required
def note_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        lifetime = request.POST.get('lifetime')

        match lifetime:
            case '1h':
                note.expires_at = timezone.now() + timedelta(hours=1)
            case '24h':
                note.expires_at = timezone.now() + timedelta(hours=24)
            case '7d':
                note.expires_at = timezone.now() + timedelta(days=7)

        note.is_burn_after_reading = 'burn_after_reading' in request.POST
        master_key = request.session.get('master_key')

        note = Note(title=title, content=content, author=request.user)
        note.save(master_key=master_key)

        return redirect('note-menu')
    return render(request, 'note-create.html')


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