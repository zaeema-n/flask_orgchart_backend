import graphene
from .queries import Query

class Mutation(graphene.ObjectType):
    pass  # You can add mutations here if needed

# schema = graphene.Schema(query=Query, mutation=Mutation) # Uncomment if you have mutations

schema = graphene.Schema(query=Query)