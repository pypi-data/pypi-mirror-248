from graphene import Boolean, Argument, Mutation
from graphene.utils.str_converters import to_snake_case
from djraphql.access_permissions import DELETE
from ....abstract_type_builder import MutationRootTypeBuilder, CacheableTypeBuilder
from ...mappings import Types


class DeleteMutation(CacheableTypeBuilder, MutationRootTypeBuilder):
    @classmethod
    def make(cls, registry, **kwargs):
        model_class = kwargs["model_class"]
        entity_class = registry.get_entity_class(model_class)
        model_name = entity_class.get_node_name()
        pk_input_type = registry.get_or_create_type(
            Types.PK_INPUT_TYPE, model_class=model_class
        )
        mutation_arguments_type = type(
            "{}DeleteArguments".format(model_name),
            (object,),
            {"pk": Argument(pk_input_type, required=True)},
        )

        return type(
            "Delete{}".format(model_name),
            (Mutation,),
            {
                "Arguments": mutation_arguments_type,
                "success": Boolean(),
                "mutate": registry.get_or_create_type(
                    Types.DELETE_MUTATION_RESOLVER, model_class=model_class
                ),
                "__doc__": cls.get_docs(entity_class),
            },
        )

    @staticmethod
    def get_field_name(entity_class):
        model_name = entity_class.get_node_name()
        return "delete_{}".format(to_snake_case(model_name))

    @classmethod
    def get_docs(cls, entity_class):
        model_name = entity_class.get_node_name()
        return """Given a {} identifier (pk), dangerously deletes the
            associated object from the database.
        """.format(
            model_name
        )

    @staticmethod
    def get_required_access_permissions():
        return DELETE
