import uuid
from django.db import models

class News(models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Título', max_length=150)
    description = models.TextField('Descrição')
    created_at = models.DateTimeField('Data de criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
