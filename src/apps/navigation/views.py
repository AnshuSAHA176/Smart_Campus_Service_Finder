from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GraphNode,GraphEdge
from rest_framework.permissions import AllowAny
from .serializer import NodeSerializer




class Test(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
       
        node = GraphNode.objects.prefetch_related('outgoing_edges','incoming_edges')
        serializer = NodeSerializer(node,many = True)

        graph = {
        data['id']: [
                        (edge["to_node"], edge["distance"])
                       for edge in data['outgoing_edges']
                    ]
            for data in serializer.data
        }

        

        return Response({
            "node":graph
            
        })


    




