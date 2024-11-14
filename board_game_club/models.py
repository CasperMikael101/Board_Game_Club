from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class BoardGame(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

class Loan(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE, related_name='loans')
    borrowed_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)

    def is_active(self):
        return self.returned_at is None

# Create your models here.
