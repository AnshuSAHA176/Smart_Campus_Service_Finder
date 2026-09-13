from django.contrib.gis.db import models as gis_models
from pgvector.django import VectorField


class Place(gis_models.Model):
    name = gis_models.CharField(max_length=150)

    description = gis_models.TextField()

    category = gis_models.CharField(max_length=50)

    location = gis_models.PointField(
        geography=True,
        srid=4326
    )

    embedding = VectorField(
        dimensions=1024,
        null=True,
        blank=True
    )

    created_at = gis_models.DateTimeField(auto_now_add=True)
    updated_at = gis_models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name