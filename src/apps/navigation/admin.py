from django.contrib import admin

from django.contrib.gis.admin import GISModelAdmin
from .models import GraphNode,GraphEdge
@admin.register(GraphNode)
class Admin_node(GISModelAdmin):
    pass
@admin.register(GraphEdge)
class Admin_node(GISModelAdmin):
    pass
