from django.core.management import BaseCommand
from notes.models import Note
from django.utils import timezone


class Command(BaseCommand):
    ...