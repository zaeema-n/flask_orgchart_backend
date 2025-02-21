from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphql_api.schema import schema


app = Flask(__name__)
CORS(app)

# Create Flask App and add GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=True)
