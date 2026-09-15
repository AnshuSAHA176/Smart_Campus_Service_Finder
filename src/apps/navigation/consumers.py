from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import GraphNode
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core.cache import cache


class LiveLocationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        cache_key = f"navigation_route:{self.user.id}"

        route_data = cache.get(cache_key)

        path = route_data["path"]

        data = json.loads(text_data)

        user_point = Point(
            data["longitude"],
            data["latitude"],
            srid=4326
        )

        node_id = [item['node'] for item in path]

        node = (GraphNode.objects.filter(id__in = node_id)
                .annotate(distance = Distance('location',user_point)).order_by('distance').first()
                )
        monitor_key = f"navigation_monitor:{self.user.id}"
        
        if node.distance.m <= 10:
            cache.set(monitor_key, 0, timeout=60)

            message = {
                "type": "navigation_status",
                "status": "on_route",
                "message": "You are following the planned route."
            }

        elif node.distance.m < 20:
                cache.set(monitor_key, 0, timeout=60)

                message = {
                    "type": "navigation_status",
                    "status": "uncertain",
                    "message": "Checking your location..."
                }

        else:
                monitor_data = cache.get(monitor_key, 0)
                monitor_data += 1
                cache.set(monitor_key, monitor_data, timeout=60)

                if monitor_data >= 6:
                    message = {
                        "type": "navigation_status",
                        "status": "off_route",
                        "message": "You appear to be off the planned route."
                    }
