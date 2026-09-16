from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import GraphNode
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point,LineString
from django.core.cache import cache
from .dijkstra import dijkstra

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

        # Get current navigation route
        cache_key = f"navigation_route:{self.user.id}"

        route_data = cache.get(cache_key)

        if not route_data:
            await self.send(
                text_data=json.dumps({
                    "type": "navigation_status",
                    "status": "no_route",
                    "message": "No active navigation route found."
                })
            )
            return

        destination_data = cache.get(f'destination_data {self.user.id}')

        if not destination_data:
               return

        destination = GraphNode.objects.filter(
            id = destination_data['destination_node']
        ).annotate(distance = Distance('location',user_point)).first()

        if not destination:
            return 

        ARRIVAL_RADIUS = 10  # meters

        if destination.distance.m <= ARRIVAL_RADIUS:

            message = {
                "type": "navigation_status",
                "status": "arrived",
                "message": "You have reached your destination."
            }

            # Send arrival message
            await self.send(
                text_data=json.dumps(message)
            )

            # Remove active navigation data
            cache.delete(
                f"navigation_route:{self.user.id}"
            )

            cache.delete(
                f"destination_data {self.user.id}"
            )

            cache.delete(
            f"navigation_monitor:{self.user.id}"
        )
            return





        

        # Get route geometry from cache
        route_geometry = route_data["route_geometry"]

        # Create LineString
        route_line = LineString(
            route_geometry,
            srid=4326
        )

        # Get frontend GPS data
        data = json.loads(text_data)

        # IMPORTANT: longitude first
        user_point = Point(
            data["longitude"],
            data["latitude"],
            srid=4326
        )

        # Calculate distance from user to route
        distance = user_point.distance(route_line)

        print("Distance from route:", distance)

        # Your monitoring logic
        monitor_key = f"navigation_monitor:{self.user.id}"

        if distance <= 10:

            cache.set(
                monitor_key,
                0,
                timeout=60
            )

            message = {
                "type": "navigation_status",
                "status": "on_route",
                "message": "You are following the planned route."
            }

        elif distance < 20:

            cache.set(
                monitor_key,
                0,
                timeout=60
            )

            message = {
                "type": "navigation_status",
                "status": "uncertain",
                "message": "Checking your location..."
            }

        else:

            monitor_data = cache.get(
                monitor_key,
                0
            )

            monitor_data += 1

            cache.set(
                monitor_key,
                monitor_data,
                timeout=60
            )

            if monitor_data >= 6:

                message = {
                    "type": "navigation_status",
                    "status": "off_route",
                    "message": "You appear to be off the planned route."
                }

                await self.send(text_data=json.dumps(message))
                nearest_node = (GraphNode.objects.annotate(distance = Distance('location',user_point)).
                                order_by('distance').first()

                                )
                
                

                path, distance = dijkstra(
                        destination_data['graph'],
                        start=nearest_node.id,
                        destination=destination_data['destination_node']
                    )
                if not path:
                    return

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
                cache_key = f"navigation_route:{self.user.id}"

                cache.set(
                    cache_key,
                    data,        #it can overwrite the existing value
                    timeout=300
                )

                await self.send(
                    text_data=json.dumps(data)
                )


            else:

                message = {
                    "type": "navigation_status",
                    "status": "checking",
                    "message": "Checking your location..."
                }

        await self.send(
            text_data=json.dumps(message)
        )

