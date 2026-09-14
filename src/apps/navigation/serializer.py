from rest_framework import serializers
from .models import GraphNode,GraphEdge




class NodeEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphEdge

        fields= ['from_node','to_node','distance']



class NodeSerializer(serializers.ModelSerializer):
    outgoing_edges = NodeEdgeSerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = GraphNode
        fields = "__all__"


