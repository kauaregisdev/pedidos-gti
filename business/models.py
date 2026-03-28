from django.db import models

class Business(models.Model):
    name = models.CharField('Nome da empresa', max_length=150)
    description = models.TextField('Descrição da empresa')
    email = models.EmailField('Email da empresa')
    phone = models.CharField('Número de telefone', max_length=20)
    founded_at = models.DateField('Data de fundação')

    class Meta:
        verbose_name = 'Dados da empresa'
        verbose_name_plural = 'Dados da empresa'

    def __str__(self):
        return self.name
