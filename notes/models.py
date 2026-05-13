from django.utils import timezone

from cryptography.fernet import Fernet
from django.db import models
from users.models import User


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_burn_after_reading = models.BooleanField(default=False)

    @property
    def is_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False

    def save(self, *args, **kwargs):
        master_key = kwargs.pop('master_key', None)
        if master_key and self.content and not self.content.startswith('gAAA'):
            cipher = Fernet(master_key.encode())
            self.content = cipher.encrypt(self.content.encode()).decode('utf-8')
        super().save(*args, **kwargs)

    @staticmethod
    def encrypt_note(text, master_key):
        if not master_key:
            return 'Error: Key not provided'
        cipher = Fernet(master_key.encode())
        return cipher.encrypt(text.encode()).decode('utf-8')

    def decrypt_note_via_password(self, master_key):
        if not master_key:
            return 'Error: Key not provided'
        cipher = Fernet(master_key.encode())
        print(cipher)
        print(self.content)
        return cipher.decrypt(self.content.encode()).decode('utf-8')

    class Meta:
        verbose_name_plural = 'Notes'

    def __str__(self):
        return self.title