from django.http import JsonResponse
from core.models import Entity
from core.services.resolution import NetworkDiscoveryService

def search_api(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    # Perform Discovery
    person = NetworkDiscoveryService.perform_osint_search(query)
    
    if not person:
        return JsonResponse({'error': 'No entity found or discovery failed'}, status=404)

    # Format graph for D3.js
    nodes = [{
        'id': person.id, 
        'name': person.value, 
        'type': person.entity_type,
        'photo': person.photo_url,
        'code': person.identifier_code
    }]
    links = []

    # Get related nodes from the database
    for rel in person.outbound_relationships.all():
        target = rel.target_entity
        nodes.append({
            'id': target.id, 
            'name': target.value, 
            'type': target.entity_type,
            'photo': target.photo_url,
            'code': target.identifier_code
        })
        links.append({'source': person.id, 'target': target.id, 'type': rel.relationship_type})

    return JsonResponse({'nodes': nodes, 'links': links})
