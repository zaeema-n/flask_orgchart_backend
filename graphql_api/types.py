import graphene

class DepartmentType(graphene.ObjectType):
    name = graphene.String()

class MinisterType(graphene.ObjectType):
    name = graphene.String()
    departments = graphene.List(DepartmentType)

class GovernmentType(graphene.ObjectType):
    name = graphene.String()
    ministers = graphene.List(MinisterType)
