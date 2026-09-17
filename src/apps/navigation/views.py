from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GraphNode,GraphEdge
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializer import NodeSerializer,NodeReturnSerializer
from .dijkstra import dijkstra
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.core.cache import cache


class ShortstPathView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
     
        latitude = request.data.get('latitude')

        longitude = request.data.get('longitude')

        destination_latitude = request.data.get('destination_latitude')

        destination_longitude = request.data.get('destination_longitude')

        user_point = Point(longitude,latitude,srid=4326)

        destination_point = Point(destination_longitude,destination_latitude,srid=4326)

        near_node = GraphNode.objects.annotate(distance=Distance('location',user_point)).order_by('distance').first()

        near_destination_node = GraphNode.objects.annotate(distance=Distance('location',destination_point)).order_by('distance').first()

        




        node = GraphNode.objects.prefetch_related('outgoing_edges','incoming_edges')

        serializer = NodeSerializer(node,many = True)

        graph = {
        data['id']: [
                        (edge["to_node"], edge["distance"])
                       for edge in data['outgoing_edges']
                    ]
            for data in serializer.data
        }

        cache.set(f'destination_data {request.user}',
                  {"destination_node":near_destination_node.id,"graph":graph})

        path, distance = dijkstra(
                graph,
                near_node.id,
                near_destination_node.id
            )

        nodes = GraphNode.objects.in_bulk(path)

        route = [
            {
                "node": node_id,
                "latitude": nodes[node_id].location.y,
                "longitude": nodes[node_id].location.x,
            }
            for node_id in path
        ]
    
        data = {
        "distance": distance,
        "path": route,
        "route_geometry": [
            (item["longitude"], item["latitude"])
            for item in route
        ],
    }
        cache_key = f"navigation_route:{request.user.id}"
            
        cache.set(cache_key,data)

        return Response(data)


        




