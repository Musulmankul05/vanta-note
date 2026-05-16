from django.core.management import BaseCommand
from notes.models import Note
from django.utils import timezone


class Command(BaseCommand):
    help = 'Cleans up expired notes.'

    def handle(self, *args, **options):
        deleted, _ = Note.objects.filter(expired_at__lt=timezone.now()).delete()
        self.stdout.write(f"Purged {deleted} expired entries.")