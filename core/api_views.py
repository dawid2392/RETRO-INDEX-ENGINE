from django.http import JsonResponse
from core.models import Entity, Relationship
from core.services.resolution import NetworkDiscoveryService

def search_api(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    # Perform Discovery
    person = NetworkDiscoveryService.perform_osint_search(query)
    
    # Format graph for D3.js
    nodes = [{'id': person.id, 'name': person.value, 'type': person.entity_type}]
    links = []

    # Get related nodes
    for rel in person.outbound_relationships.all():
        target = rel.target_entity
        nodes.append({'id': target.id, 'name': target.value, 'type': target.entity_type})
        links.append({'source': person.id, 'target': target.id, 'type': rel.relationship_type})

    return JsonResponse({'nodes': nodes, 'links': links})
