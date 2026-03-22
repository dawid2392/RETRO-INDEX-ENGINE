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

class Relationship(models.Model):
    RELATIONSHIP_TYPES = (
        ('OWNED_BY', 'Owned By'),
        ('ASSOCIATED_WITH', 'Associated With'),
        ('COMMUNICATED_WITH', 'Communicated With'),
    )
    source_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='outbound_relationships')
    target_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='inbound_relationships')
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    weight = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source_entity', 'target_entity', 'relationship_type')

    def __str__(self):
        return f"{self.source_entity} -[{self.relationship_type}]-> {self.target_entity}"
