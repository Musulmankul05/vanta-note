from django.contrib import admin

from notes.models import Note


# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'author')
    list_display = ('title', 'author')