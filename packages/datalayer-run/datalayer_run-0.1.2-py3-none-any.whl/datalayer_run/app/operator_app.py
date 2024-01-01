"""
- API         https://github.com/jupyterhub/configurable-http-proxy#using-the-rest-api
- Swagger API http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyterhub/configurable-http-proxy/master/doc/rest-api.yml#/default

The configurable-http-proxy REST API is documented and available as:

- a nicely rendered, interactive version at the petstore swagger site
- a swagger specification file in this repo

HTTP method Endpoint                  Function
GET	        /api/routes               Get all routes in routing table
POST        /api/routes/{route_spec}  Add a new route
DELETE      /api/routes/{route_spec}  Remove the given route

Authenticating via passing a token
The REST API is authenticated via passing a token in the Authorization header. The API is served under the /api/routes base URL.
For example, this curl command entered in the terminal passes this header "Authorization: token $CONFIGPROXY_AUTH_TOKEN" for authentication and retrieves the current routing table from this endpoint, http://localhost:8001/api/routes:

curl -H "Authorization: token $CONFIGPROXY_AUTH_TOKEN" http://localhost:8001/api/routes

Getting the routing table
Request:
GET /api/routes[?inactive_since=ISO8601-timestamp]
Parameters:
inactive_since: If the inactive_since URL parameter is given as an ISO8601 timestamp, only routes whose last_activity is earlier than the timestamp will be returned. The last_activity timestamp is updated whenever the proxy passes data to or from the proxy target.
Response:
Status code
status: 200 OK
Response body
A JSON dictionary of the current routing table. This JSON dictionary excludes the default route.
Behavior: The current routing table is returned to the user if the request is successful.

Adding new routes
POST requests create new routes. The body of the request should be a JSON dictionary with at least one key: target, the target host to be proxied.
Request:
POST /api/routes/[:path]
Required input:
target: The host URL
Example request body:
{
  "target": "http://localhost:8002"
}
Response:
status: 201 Created
Behavior: After adding the new route, any request to /path/prefix on the proxy's public interface will be proxied to target.

Deleting routes
Request:
DELETE /api/routes/[:path]
Response:
status: 204 No Content
Behavior: Removes a route from the proxy's routing table.
"""

import json
import warnings

from datalayer.application import NoStart
from tornado.httpclient import HTTPClient
from tornado.escape import json_decode, json_encode

from ..application_base import DatalayerRunBaseApp



class RoutesListApp(DatalayerRunBaseApp):
    """An application to list the routes."""

    description = """
      An application to list the routes.
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def get_routes(self):
        client = HTTPClient()
        response = client.fetch(
            self.router_url,
            headers={
                "Authorization": f"token {self.router_token}",
            },
            method='GET',
        )
        routes = json_decode(response.body)
        self.log.info("Routes %s", json.dumps(routes, indent=2))
        client.close()
        return routes

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for routes list.")
            self.exit(1)
        self.get_routes()


class RouteDeleteApp(DatalayerRunBaseApp):
    """An application to delete a route."""

    description = """
      An application to delete a routes.
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def delete_route(self, route):
        client = HTTPClient()
        response = client.fetch(
            self.router_url + route,
            headers={
                "Authorization": f"token {self.router_token}",
            },
            method='DELETE',
        )
        self.log.info("Route deleted %s %s", route, response)
        client.close()

    def start(self):
        """Start the app."""
        if len(self.extra_args) != 1:
            warnings.warn("Too many arguments were provided for routes list.")
            self.exit(1)
        self.delete_route(self.extra_args[0])


class RouteCreateApp(DatalayerRunBaseApp):
    """An application to create a route."""

    description = """
      An application to create a routes.
    """

    def initialize(self, *args, **kwargs):
        """Initialize the app."""
        super().initialize(*args, **kwargs)

    def create_route(self, route, target):
        client = HTTPClient()
        response = client.fetch(
            self.router_url + route,
            headers={
                "Authorization": f"token {self.router_token}",
            },
            method='POST',
            body=json_encode({
                "target": target,
            })
        )
        self.log.info("Route created %s %s %s", route, target, response)
        client.close()

    def start(self):
        """Start the app."""
        if len(self.extra_args) != 2:
            warnings.warn("Too many arguments were provided for routes list.")
            self.exit(1)
        self.create_route(self.extra_args[0], self.extra_args[1])


class RunApp(DatalayerRunBaseApp):
    """A Router application."""

    description = """
      The Datalayer Run application for the Router.
    """

    subcommands = {
        "list": (RoutesListApp, RoutesListApp.description.splitlines()[0]),
        "create": (RouteCreateApp, RouteCreateApp.description.splitlines()[0]),
        "delete": (RouteDeleteApp, RouteDeleteApp.description.splitlines()[0]),
    }

    def start(self):
        try:
            super().start()
            self.log.error(f"One of `{'`, `'.join(RunApp.subcommands.keys())}` must be specified.")
            self.exit(1)
        except NoStart:
            pass
        self.exit(0)
