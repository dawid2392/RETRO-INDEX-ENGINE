from django.contrib import admin
from .models import Source, Entity

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'value', 'source', 'confidence_score', 'created_at')
    list_filter = ('entity_type', 'source', 'created_at')
    search_fields = ('value',)