import graphene
from .types import GovernmentType
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

class Query(graphene.ObjectType):
    govStrucByDate = graphene.Field(graphene.List(GovernmentType), date=graphene.String(required=True))

    def resolve_govStrucByDate(self, info, date):
        query = """
        MATCH (g:government)-[r:GOVERNS]->(m:minister)-[y:GOVERNS]->(d:department)
        WHERE (r.type = "AS_MINISTER") AND (y.type= "AS_DEPARTMENT")
        AND (r.start_date <= date($date) AND (r.end_date IS NULL OR r.end_date > date($date)))
        AND (y.start_date <= date($date) AND (y.end_date IS NULL OR y.end_date > date($date)))
        RETURN g.name AS government, m.name AS minister, d.name AS department
        """

        with driver.session() as session:
            result = session.run(query, date=date)
            records = result.data()

        # Restructure data into hierarchical format
        gov_dict = {}
        for record in records:
            gov_name = record["government"]
            min_name = record["minister"]
            dep_name = record["department"]

            if gov_name not in gov_dict:
                gov_dict[gov_name] = {"name": gov_name, "ministers": {}}

            if min_name not in gov_dict[gov_name]["ministers"]:
                gov_dict[gov_name]["ministers"][min_name] = {
                    "name": min_name,
                    "departments": [],
                }

            gov_dict[gov_name]["ministers"][min_name]["departments"].append(
                {"name": dep_name}
            )

        # Convert to list format for GraphQL response
        return [
            {
                "name": gov["name"],
                "ministers": list(gov["ministers"].values()),
            }
            for gov in gov_dict.values()
        ]
