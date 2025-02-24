from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphql_api.schema import schema
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
CORS(app)

# Create Flask App and add GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

# Swagger UI Configuration
SWAGGER_URL = "/api/docs"  # Swagger UI will be available at this endpoint
API_URL = "/openapi/openapi.yaml"  # Path to your OpenAPI file

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve OpenAPI YAML File
@app.route("/openapi/openapi.yaml")
def serve_openapi():
    return send_from_directory("openapi", "openapi.yaml")

if __name__ == "__main__":
    app.run(debug=True)
