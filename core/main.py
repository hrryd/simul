import sys
import tempfile
import shutil
from distutils.dir_util import copy_tree
import docker
from kubernetes import client, config
import yaml
from os import path
import uuid
from pprint import pprint
import argparse

def pre_process(src_dir, out_dir):
    copy_tree(src_dir, out_dir)
    shutil.copy('Dockerfile', out_dir)

def build_image(src_dir):
    client = docker.from_env()
    print('Building Docker image')
    client.images.build(path=src_dir, tag='app:1.0')

def read_config(src_dir):
    with open(path.join(src_dir, "sim.yaml"), 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)

def create_namespace(api_client, namespace):
    metadata = client.V1ObjectMeta(name=namespace)
    body = client.V1Namespace(metadata=metadata)
    api_client.create_namespace(body=body)

def create_log_server(core_v1, apps_v1, namespace):
    with open(path.join(path.dirname(__file__), "kubernetes", "log-server-service.yaml")) as f:
        service_yaml = yaml.safe_load(f)

    with open(path.join(path.dirname(__file__), "kubernetes", "log-server-deployment.yaml")) as f:
        deployment_yaml = yaml.safe_load(f)

    core_v1.create_namespaced_service(body=service_yaml, namespace=namespace)
    apps_v1.create_namespaced_deployment(body=deployment_yaml, namespace=namespace)

def create_frontend_server(core_v1, apps_v1, namespace):
    with open(path.join(path.dirname(__file__), "kubernetes", "frontend-service.yaml")) as f:
        service_yaml = yaml.safe_load(f)

    with open(path.join(path.dirname(__file__), "kubernetes", "frontend-deployment.yaml")) as f:
        deployment_yaml = yaml.safe_load(f)

    core_v1.create_namespaced_service(body=service_yaml, namespace=namespace)
    apps_v1.create_namespaced_deployment(body=deployment_yaml, namespace=namespace)

def create_fluentd(core_v1, apps_v1, namespace):
    with open(path.join(path.dirname(__file__), "kubernetes", "fluentd-config.yaml")) as f:
        config_yaml = yaml.safe_load(f)

    with open(path.join(path.dirname(__file__), "kubernetes", "fluentd-daemonset.yaml")) as f:
        daemonset_yaml = yaml.safe_load(f)

    core_v1.create_namespaced_config_map(body=config_yaml, namespace=namespace)
    apps_v1.create_namespaced_daemon_set(body=daemonset_yaml, namespace=namespace)

def create_service(api_client, namespace):
    with open(path.join(path.dirname(__file__), "kubernetes", "app-service.yaml")) as f:
        service_yaml = yaml.safe_load(f)

    api_client.create_namespaced_service(body=service_yaml, namespace=namespace)

def create_deployment(api_client, namespace, replicas, latency, dropRate):
    # Container
    pod_ip_fs = client.V1ObjectFieldSelector(field_path="status.podIP")
    pod_ip_src = client.V1EnvVarSource(field_ref=pod_ip_fs)
    pod_ip_env = client.V1EnvVar(name="POD_IP", value_from=pod_ip_src)

    pod_ns_fs = client.V1ObjectFieldSelector(field_path="metadata.namespace")
    pod_ns_src = client.V1EnvVarSource(field_ref=pod_ns_fs)
    pod_ns_env = client.V1EnvVar(name="POD_NAMESPACE", value_from=pod_ns_src)

    app_container_spec = client.V1Container(name="app", image="app:1.0", command=["python3"], 
        args=["app.py", str(replicas), "$(POD_IP)", "$(POD_NAMESPACE)"], env=[pod_ip_env, pod_ns_env])

    # HAProxy Container
    haproxy_container_spec = client.V1Container(name="haproxy", image="app-haproxy:1.0")

    # App Proxy Container
    app_proxy_container_spec = client.V1Container(name="goproxy", image="app-proxy:1.0", 
        args=[str(replicas), "$(POD_NAMESPACE)", str(latency), str(dropRate)], env=[pod_ns_env])

    # Pod
    pod_spec = client.V1PodSpec(termination_grace_period_seconds=10, 
        containers=[app_container_spec, haproxy_container_spec, app_proxy_container_spec])
    pod_metadata = client.V1ObjectMeta(labels={"app": "app-service"})
    pod_template_spec = client.V1PodTemplateSpec(metadata=pod_metadata, spec=pod_spec)

    # StatefulSet
    statefulset_selector = client.V1LabelSelector(match_labels={"app": "app-service"})
    statefulset_spec = client.V1StatefulSetSpec(replicas=replicas, pod_management_policy="Parallel", 
        service_name="app-service", selector=statefulset_selector, template=pod_template_spec)
    statefulset_metadata = client.V1ObjectMeta(name="app")
    deployment = client.V1StatefulSet(api_version="apps/v1", metadata=statefulset_metadata, spec=statefulset_spec)

    # Deploy
    api_client.create_namespaced_stateful_set(body=deployment, namespace=namespace)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp_dir:
        pre_process(args.directory, tmp_dir)
        build_image(tmp_dir)
        sim_config = read_config(tmp_dir)
        print('Config', sim_config)

    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    apps_v1_ext = client.ExtensionsV1beta1Api()

    namespace = uuid.uuid4().hex

    print('Create namespace', namespace)
    create_namespace(core_v1, namespace)

    print('Create log server')
    create_log_server(core_v1, apps_v1, namespace)

    print('Create fluentd')
    create_fluentd(core_v1, apps_v1_ext, namespace)

    print('Create frontend server')
    create_frontend_server(core_v1, apps_v1, namespace)

    print('Create app service')
    create_service(core_v1, namespace)

    print('Create app deployment')
    latency = sim_config.get('latency', 0)
    dropRate = sim_config.get('dropRate', 0)
    create_deployment(apps_v1, namespace, sim_config['replicas'], latency, dropRate)