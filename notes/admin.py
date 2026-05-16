from django.contrib import admin

from notes.models import Note


# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'author', 'is_burn_after_reading')
    list_display = ('title', 'author')