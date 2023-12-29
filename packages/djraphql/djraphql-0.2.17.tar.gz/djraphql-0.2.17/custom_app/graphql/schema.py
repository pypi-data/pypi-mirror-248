from graphene import Int
from djraphql.fields import AllModelFields, ModelField
from djraphql.entities import Entity
from djraphql.access_permissions import (
    C,
    R,
    U,
    D,
)
from custom_app.models import (
    Artist,
    Label,
)

class CustomLabelEntity(Entity):
    class Meta:
        model = Label
        custom_node_name = "CustomLabel"
        fields = (
            AllModelFields(),
            ModelField("id", graphene_type=Int),
        )

    access_permissions = (C, R, U, D)


class CustomArtistEntity(Entity):
    class Meta:
        model = Artist
        custom_node_name = "CustomArtist"
        fields = (
            AllModelFields(),
            ModelField("id", graphene_type=Int),
        )

    access_permissions = (C, R, U, D)

