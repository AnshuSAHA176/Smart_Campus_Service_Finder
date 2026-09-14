from django.contrib.gis.db import models


class GraphNode(models.Model):
    id = models.IntegerField(primary_key=True)

    location = models.PointField(
        srid=4326,
        geography=True
    )

    class Meta:
        db_table = "graph_nodes"

    def __str__(self):
        return f"Node {self.id}"


class GraphEdge(models.Model):
    from_node = models.ForeignKey(
        GraphNode,
        on_delete=models.CASCADE,
        related_name="outgoing_edges"
    )

    to_node = models.ForeignKey(
        GraphNode,
        on_delete=models.CASCADE,
        related_name="incoming_edges"
    )

    distance = models.FloatField()

    class Meta:
        db_table = "graph_edges"

        constraints = [
            models.UniqueConstraint(
                fields=["from_node", "to_node"],
                name="unique_graph_edge"
            )
        ]

    def __str__(self):
        return f"{self.from_node_id} -> {self.to_node_id}"
