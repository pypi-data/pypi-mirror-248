# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

"""Datalayer Run service for Kubernetes."""

import os
import logging

import yaml
from kubernetes import client, config, utils

logger = logging.getLogger("__name__")


try:
  config.load_incluster_config()
except:
  config.load_kube_config()


DATALAYER_RUN = os.environ.get("DATALAYER_RUN")


def create_pod_service(namespace, name):
    manifests = yaml.safe_load(f"""
apiVersion: v1
kind: Pod
metadata:
  name: {name}
  namespace: {namespace}
  labels:
    app: jupyterpool
spec:
  hostname: {name}
  subdomain: jupyterpool
  containers:
  - name: jupyterpool
    image: datalayer/jupyterpool:0.0.8
    imagePullPolicy: Always
    ports:
    - containerPort: 2300
      protocol: TCP
""")
    api_response = client.CoreV1Api().create_namespaced_pod(body=manifests, namespace=namespace)
    """
    while True:
        try:
            api_response = v1.read_namespaced_pod(name=name, namespace=namespace)
            if api_response.status.phase != 'Pending':
                break
            time.sleep(1)
        except ApiException as e:
            print(e)
            time.sleep(1)
    """
    logger.info(f'Pod {name} in {namespace} is created: {api_response}')


def __create_jupyter_server_manifest(user_handle, namespace, jupyter_server_name):
    display_name = f"jupyter-server-{user_handle}-{jupyter_server_name}"
    path = f"{user_handle}/{jupyter_server_name}"
    token = hex(abs(hash(user_handle))).replace("0x", "")
    docker_image = "datalayer/jupyter-server-kernels:0.0.8"
    specs = f"""
apiVersion: v1
kind: Pod
metadata:
  name: {display_name}
  namespace: {namespace}
  labels:
    jupyter-server: {display_name}
    subdomain: jupyter-server
spec:
  hostname: {display_name}
  subdomain: jupyter-server
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: datalayer.io/role
            operator: In
            values:
            - jupyter
          - key: datalayer.io/xpu
            operator: In
            values:
            - cpu
  containers:
  - image: {docker_image}
    imagePullPolicy: Always
    name: jupyter-server
    ports:
      - containerPort: 2300
        protocol: TCP
    env:
      - name: JUPYTER_BASE_URL
        value: "/jupyter/server/{path}"
      - name: JUPYTER_TOKEN
        value: "{token}"
#    resources:
#      requests:
#        cpu: "250m"
#        memory: "64Mi"
#      limits:
#        cpu: "500m"
#        memory: "128Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: jupyter-server
  namespace: datalayer
spec:
  selector:
    subdomain: jupyter-server
  clusterIP: None
  ports:
  - name: jupyter-server
    port: 1234
---
apiVersion: v1
kind: Service
metadata:
  name: jupyter-kernel
  namespace: datalayer
spec:
  selector:
    subdomain: jupyter-kernel
  clusterIP: None
  ports:
  - name: jupyter-kernel
    port: 1234
---
apiVersion: v1
kind: Service
metadata:
  name: {display_name}-svc
  namespace: datalayer
  labels:
    jupyter-server: {display_name}
    subdomain: jupyter-server
spec:
  type: ClusterIP
  ports:
  - port: 2300
    name: {display_name}-http
  selector:
    jupyter-server: {display_name}
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {display_name}-ingress
  namespace: datalayer
  labels:
    jupyter-server: {display_name}
    subdomain: jupyter-server
  annotations:
    kubernetes.io/ingress.class: 'nginx'
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/affinity: cookie
    nginx.ingress.kubernetes.io/affinity-mode: persistent
    nginx.ingress.kubernetes.io/session-cookie-expires: '172800'
    nginx.ingress.kubernetes.io/session-cookie-max-age: '172800'
    nginx.ingress.kubernetes.io/session-cookie-samesite: None
    nginx.ingress.kubernetes.io/session-cookie-name: router-affinity
    cert-manager.io/acme-challenge-type: 'http01'
spec:
  tls:
  - hosts:
    - {DATALAYER_RUN}
    secretName: {DATALAYER_RUN}-router-cert-secret
  rules:
  - host: {DATALAYER_RUN}
    http:
      paths:
      - path: /jupyter/server/{path}
        pathType: Prefix
        backend:
          service:
            name: {display_name}-svc
            port: 
              number: 2300
"""
    return specs, display_name, path, token


def create_jupyter_server_service(user_handle, namespace, jupyter_server_name):
    specs, display_name, path, token = __create_jupyter_server_manifest(user_handle, namespace, jupyter_server_name)
    manifests = yaml.safe_load_all(specs)
    try:
      res = utils.create_from_yaml(
        client.ApiClient(),
        yaml_objects = manifests,
        namespace = namespace,
      )
      logger.info(f'Jupyter Server {jupyter_server_name} in {namespace} for user {user_handle} is created: {res}')
    except Exception as err:
       logger.error(err)
    return {
       "display_name": display_name,
       "path": path,
       "token": token,
       "ingress": f"https://{DATALAYER_RUN}/jupyter/server/{path}",
    }


def delete_jupyter_server_service(user_handle, namespace, jupyter_server_name):
    try:
      client.CoreV1Api().delete_namespaced_pod(
          f"jupyter-server-{user_handle}-{jupyter_server_name}",
          namespace = namespace,
      )
    except Exception as err:
       logger.error(err)
    try:
      client.CoreV1Api().delete_namespaced_service(
          f"jupyter-server-{user_handle}-{jupyter_server_name}-svc",
          namespace = namespace,     
      )
    except Exception as err:
       logger.error(err)
    try:
      client.NetworkingV1Api().delete_namespaced_ingress(
          f"jupyter-server-{user_handle}-{jupyter_server_name}-ingress",
          namespace = namespace,
      )
    except Exception as err:
       logger.error(err)


def list_pods_all_namespaces_service():
    return client.CoreV1Api().list_pod_for_all_namespaces(watch=False)