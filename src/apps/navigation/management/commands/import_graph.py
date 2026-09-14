import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from apps.navigation.models import GraphNode, GraphEdge


class Command(BaseCommand):

    help = "Import Raiganj University navigation graph"

    def handle(self, *args, **options):

        file_path = (
            Path(__file__).resolve()
            .parents[3]
            / "data"
            / "raiganj_university_graph.json"
        )

        self.stdout.write(
            f"Reading graph from: {file_path}"
        )

        with open(file_path, "r") as file:
            data = json.load(file)

        nodes_data = data["nodes"]
        graph_data = data["graph"]

        self.stdout.write(
            f"Nodes found: {len(nodes_data)}"
        )

        # --------------------------------
        # Delete existing graph
        # --------------------------------

        GraphEdge.objects.all().delete()
        GraphNode.objects.all().delete()

        # --------------------------------
        # Create nodes
        # --------------------------------

        nodes = {}

        for node_id, node_data in nodes_data.items():

            latitude = node_data["latitude"]
            longitude = node_data["longitude"]

            node = GraphNode.objects.create(
                id=int(node_id),
                location=Point(
                    longitude,
                    latitude,
                    srid=4326
                )
            )

            nodes[int(node_id)] = node

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(nodes)} nodes"
            )
        )

        # --------------------------------
        # Create edges
        # --------------------------------

        edges = []

        for from_node_id, neighbours in graph_data.items():

            from_node_id = int(from_node_id)

            from_node = nodes[from_node_id]

            for to_node_id, distance in neighbours:

                to_node_id = int(to_node_id)

                to_node = nodes[to_node_id]

                edges.append(
                    GraphEdge(
                        from_node=from_node,
                        to_node=to_node,
                        distance=distance
                    )
                )

        GraphEdge.objects.bulk_create(
            edges,
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(edges)} edges"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Graph imported successfully!"
            )
        )