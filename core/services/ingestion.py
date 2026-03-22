from django.db import transaction
from core.models import Source, Entity, IdentityProfile

class IngestionService:
    @staticmethod
    def ingest_data(source_name, entity_type, value, profile_data=None):
        """
        Aggregates and normalizes data into the system, optionally linking it to an IdentityProfile.
        """
        with transaction.atomic():
            source, _ = Source.objects.get_or_create(name=source_name)
            
            profile = None
            if profile_data:
                profile, _ = IdentityProfile.objects.get_or_create(
                    full_name=profile_data.get('full_name', 'Unknown'),
                    defaults={'description': profile_data.get('description', '')}
                )
            
            entity, created = Entity.objects.get_or_create(
                entity_type=entity_type,
                value=value,
                source=source,
                defaults={'profile': profile}
            )
            
            if not created and profile:
                entity.profile = profile
                entity.save()
                
            return entity