from django.contrib import admin
from .models import Source, Entity, IdentityProfile, Relationship

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'value', 'source', 'confidence_score', 'created_at')
    list_filter = ('entity_type', 'source', 'created_at')
    search_fields = ('value',)

@admin.register(IdentityProfile)
class IdentityProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created_at')
    search_fields = ('full_name',)

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('source_entity', 'target_entity', 'relationship_type', 'created_at')
    list_filter = ('relationship_type', 'created_at')
    search_fields = ('source_entity__value', 'target_entity__value')
