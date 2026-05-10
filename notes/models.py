from cryptography.fernet import Fernet
from django.db import models
from users.models import User


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    @staticmethod
    def encrypt_note(text, master_key):
        if not master_key:
            return 'Error: Key not provided'
        cipher = Fernet(master_key.encode())
        return cipher.encrypt(text.encode()).decode('utf-8')

    def decrypt_note(self, master_key):
        if not master_key:
            return 'Error: Key not provided'
        cipher = Fernet(master_key.encode())
        return cipher.decrypt(self.content).decode('utf-8')

    class Meta:
        verbose_name_plural = 'Notes'

    def __str__(self):
        return self.title