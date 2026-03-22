from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Entity(models.Model):
    ENTITY_TYPES = (
        ('PERSON', 'Person'),
        ('EMAIL', 'Email'),
        ('USERNAME', 'Username'),
        ('IP', 'IP Address'),
    )
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)
    value = models.CharField(max_length=255, db_index=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='entities')
    confidence_score = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entities"
        unique_together = ('entity_type', 'value', 'source')

    def __str__(self):
        return f"{self.entity_type}: {self.value}"