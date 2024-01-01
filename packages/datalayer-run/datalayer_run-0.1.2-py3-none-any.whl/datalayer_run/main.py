# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

"""Datalayer Run endpoints."""

import logging
import os

from flask import (
    Flask,
    jsonify,
    send_from_directory,
)

from flask_cors import CORS

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
)

from datalayer_dao import DATALAYER_FAVICO

from datalayer_iam.services.user_service import (
    User,
)

from datalayer_run.services.kubernetes_service import (
    create_pod_service,
    create_jupyter_server_service,
    delete_jupyter_server_service,
    list_pods_all_namespaces_service,
)


ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/.."

PORT = 2111


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    force=True,
)

logging.getLogger("pysolr").setLevel(logging.CRITICAL)

logger = logging.getLogger("__name__")


app = Flask(__name__, static_folder=ROOT_FOLDER)

app.config.update(
    {
        "JWT_SECRET_KEY": os.environ["DATALAYER_JWT_SECRET"],
        "SECRET_KEY": os.environ["DATALAYER_JWT_SECRET"],
        "TESTING": True,
        "DEBUG": True,
    }
)

CORS(
    app,
    supports_credentials=True,
    # resources={r"/*": {"origins": "*"}},
    # send_wildcard=True,
)

jwt = JWTManager(app)


# Flask JWT.


def user_identity_lookup(user: User) -> dict:
    """This function that will be called whenever create_access_token
    is used. It will take whatever object is passed into the
    create_access_token method, and lets us define what the identity
    of the access token should be.
    """
    return {
        "uid": user.uid,
        "handle": user.handle,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "display_name": user.display_name(),
    }


@jwt.user_lookup_loader
def user_loader_callback(_jwt_header, identity: dict) -> User:
    """This function is called whenever a protected endpoint is accessed,
    and must return an object based on the tokens identity.
    This is called after the token is verified, so you can use
    get_jwt_claims() in here if desired. Note that this needs to
    return None if the user could not be loaded for any reason,
    such as not being found in the underlying data store
    """
    return User(
        uid=identity.get("sub").get("uid", ""),
        handle=identity.get("sub").get("handle", ""),
        email=identity.get("sub").get("email", ""),
        first_name=identity.get("sub").get("first_name", ""),
        last_name=identity.get("sub").get("last_name", ""),
        roles=identity.get("sub").get("roles", []),
    )


# Anonymous API Endpoints.


# Authenticated API endpoints.


@app.route("/api/operator/pods", methods=["GET"])
@jwt_required()
def list_pods_endpoint():
    """List pods endpoint."""
    res = list_pods_all_namespaces_service()
    pods = [f"{i.status.pod_ip} {i.metadata.namespace} {i.metadata.name}" for i in res.items]
    return jsonify(
        {
            "success": True,
            "message": "Pods list.",
            "pods": pods,
        }
    )


@app.route("/api/operator/jupyter/server/<jupyter_server_name>", methods=["POST"])
@jwt_required()
def create_jupyter_server_endpoint(jupyter_server_name):
    """Create a Jupyter Server."""
    identity = get_jwt_identity()
    user_handle = identity["handle"]
    juyter_server = create_jupyter_server_service(user_handle, "datalayer", jupyter_server_name)
    return jsonify(
        {
            "success": True,
            "message": "The Jupyter Server is created.",
            "jupyter-server": juyter_server
        }
    )


@app.route("/api/operator/jupyter/server/<jupyter_server_name>", methods=["DELETE"])
@jwt_required()
def delete_jupyter_server_endpoint(jupyter_server_name):
    """Delete a Jupyter Server."""
    identity = get_jwt_identity()
    user_handle = identity["handle"]
    delete_jupyter_server_service(user_handle, "datalayer", jupyter_server_name)
    return jsonify(
        {
            "success": True,
            "message": "The Jupyter Server is deleted.",
            "jupyter-server": {
                "name": jupyter_server_name
            }
        }
    )


@app.route("/api/operator/pod/<namespace>/<pod_name>", methods=["POST"])
@jwt_required()
def create_pod_endpoint(namespace, name):
    """Create pod endpoint."""
    create_pod_service(namespace, name)
    return jsonify(
        {
            "success": True,
            "message": "The pod is created.",
            "namespace": namespace,
            "name": name,
        }
    )


# Public catch all routes


@app.route("/api/operator/version", methods=["GET"])
def index_endpoint():
    """index"""
    return f"""<html>
  <head>
    <title>Datalayer Run Ξ Elastic Jupyter Kernels</title>
    <link rel="shortcut icon" href="{DATALAYER_FAVICO}" type="image/x-icon">
  </head>
  <body>
    <h1>Datalayer Run</h1>
    <img src="/api/operator/res/operator.svg" width="200" />
  </body>
</html>
"""


@app.route("/api/operator/res/<path:path>", defaults={"folder": "res"})
def ressource_endpoint(folder, path):
    """Ressource endpoint."""
    return send_from_directory(ROOT_FOLDER + "/" + folder, path)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all_endpoint(path):
    """Catch all."""
    logger.info("Catch all for path [%s]", path)
    return send_from_directory(ROOT_FOLDER, "index.html")


# Catch All Exceptions


@app.errorhandler(Exception)
def all_exception_handler(exception):
    """All exception handler."""
    logger.info("-------------------------")
    #    traceback.print_exc()
    #    logger.info(traceback.extract_stack(e))
    logger.exception(exception)
    logger.info("-------------------------")
    #    return 'Server Error', 500
    return jsonify(
        {
            "success": False,
            "message": "Server Error",
            "exception": exception,
        }
    )


# Main.

def main():
    """Main method."""
    logger.info("Server listening on port %s - Browse http://localhost:%s", PORT, PORT)
    app.run(
        debug=True,
        host="0.0.0.0",
        port=PORT,
        threaded=True,
        processes=1,
    )

if __name__ == "__main__":
    main()
