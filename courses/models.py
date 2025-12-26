from django.db import models


class Term(models.Model):
    """Lug'at atamasi"""
    title = models.CharField(max_length=200, verbose_name="Atama")
    description = models.TextField(verbose_name="Ta'rif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0, verbose_name="Tartib")
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Atama"
        verbose_name_plural = "Atamalar"
    
    def __str__(self):
        return self.title