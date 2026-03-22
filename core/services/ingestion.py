from django.db import transaction
from core.models import Source, Entity

class IngestionService:
    @staticmethod
    def ingest_data(source_name, entity_type, raw_data):
        """
        Aggregates and normalizes raw data into the system.
        """
        with transaction.atomic():
            source, _ = Source.objects.get_or_create(name=source_name)
            
            # Simple normalization logic: assume raw_data is a dict
            # In a real scenario, this would be more complex depending on source schema
            identifier = raw_data.get('identifier')
            if not identifier:
                raise ValueError("Missing identifier in raw_data")
            
            entity, created = Entity.objects.get_or_create(
                identifier=identifier,
                entity_type=entity_type,
                defaults={'source': source, 'metadata': raw_data.get('metadata', {})}
            )
            
            if not created:
                # Update existing entity metadata
                entity.metadata.update(raw_data.get('metadata', {}))
                entity.save()
                
            return entity
