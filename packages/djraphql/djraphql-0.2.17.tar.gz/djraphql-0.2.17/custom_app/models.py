from django.db import models


class Label(models.Model):
    name = models.CharField(null=False, max_length=512)
    established_year = models.IntegerField()
    website = models.URLField(null=False)

    class Meta:
        db_table = "custom_label"


class Artist(models.Model):
    name = models.CharField(null=False, max_length=512)
    year_started = models.IntegerField()
    label = models.ForeignKey(
        Label, null=True, related_name="custom_artists", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "custom_artist"
