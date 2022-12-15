import json
from dataclasses import dataclass
from logging import info, debug
from os import path
from time import sleep
from typing import Dict

import typer

from . import util_yaml as yaml
from .kubernetes_integration import KubernetesIntegration

BENCHMARK_NAMESPACE = "network-benchmarks"


class LocustBenchmark:
    def __init__(self, client_node, server_node):
        self.client_node = client_node
        self.server_node = server_node
        self.k8 = KubernetesIntegration(namespace="default")
        self.server_resources = yaml.load_to_dicts("benchmarks/locust/server-locust.yaml")
        self.client_resources = yaml.load_to_dicts("benchmarks/locust/client-locust.yaml")

    def run(self) -> dict:
        """Run the iperf3 benchmark and return the results as a dict, from the json parsed output"""
        try:
            benchmark = self.locust_benchmark()
            self.cleanup()
            return benchmark
        except KeyboardInterrupt as e:
            info("Keyboard interrupt, cleaning up")
            self.cleanup()
            raise e


    def locust_benchmark(self):
        debug("Running iperf3 benchmark on Kubernetes")
        self.deploy_server()
        return self.deploy_client()

    def deploy_server(self):
        deployment, service = self.server_resources
        nodeSelector = {"kubernetes.io/hostname": self.server_node}
        deployment["spec"]["template"]["spec"]["nodeSelector"] = nodeSelector
        self.cleanup()
        # Create deployment
        # self.wait_for_resource(service, "Service")
        info("Creating server deployment")
        self.k8.create_from_dict(deployment)
        info("Creating server service")
        self.k8.create_from_dict(service)

        info("Waiting: Server not ready")
        self.k8.wait_for_resource(deployment, "Deployment")
        nginx_locust_server = {"meta": {"name": "locust-server"}}
        self.k8.wait_for_resource(nginx_locust_server, "Service")
        sleep(1)

    def deploy_client(self):
        job = self.client_resources[0]
        nodeSelector = {"kubernetes.io/hostname": self.client_node}
        job["spec"]["template"]["spec"]["nodeSelector"] = nodeSelector
        if self.k8.exists_in_kubernetes(job, "Job"):
            self.k8.delete_job(job)
            debug("Job already exists, deleting it")
        # Create job
        sleep(2)
        info("Creating client benchmark job")
        self.k8.create_from_dict(job)
        debug(f"Job `{job['metadata']['name']}` created.")

        return self.k8.get_job_logs(job)

    def cleanup(self):
        deployment, service = self.server_resources
        if self.k8.exists_in_kubernetes(deployment, "Deployment"):
            self.k8.delete_deployment(deployment)
            self.k8.wait_for_deletion(deployment, "Deployment")
        if self.k8.exists_in_kubernetes(service, "Service"):
            self.k8.delete_service(service)
            self.k8.wait_for_deletion(service, "Service")

        job = self.client_resources[0]
        if self.k8.exists_in_kubernetes(job, "Job"):
            self.k8.delete_job(job)
            self.k8.wait_for_deletion(job, "Job")


class IPerfBenchmark:
    def __init__(self, client_node, server_node):
        self.client_node = client_node
        self.server_node = server_node
        self.k8 = KubernetesIntegration(namespace="default")
        self.server_resources = yaml.load_to_dicts("benchmarks/bandwidth/iperf3-server.yaml")
        self.client_resources = yaml.load_to_dicts("benchmarks/bandwidth/iperf3-client.yaml")

    def run(self) -> dict:
        """Run the iperf3 benchmark and return the results as a dict, from the json parsed output"""
        try:
            benchmark = self.iperf3_benchmark_kubernetes(self.client_node, self.server_node)
            return benchmark
        except KeyboardInterrupt as e:
            info("Keyboard interrupt, cleaning up")
            self.cleanup()
            raise e
        else:
            self.cleanup()

    def iperf3_benchmark_kubernetes(self, client_node, server_node):

        info("Running iperf3 benchmark on Kubernetes")

        self.deploy_server(server_node)

        return self.deploy_client(client_node)

    def deploy_server(self, server_node):
        deployment, service = self.server_resources
        nodeSelector = {"kubernetes.io/hostname": server_node}
        deployment["spec"]["template"]["spec"]["nodeSelector"] = nodeSelector
        self.cleanup()
        # Create deployment
        # self.wait_for_resource(service, "Service")
        info("Creating server deployment")
        self.k8.create_from_dict(deployment)
        info("Creating server service")
        self.k8.create_from_dict(service)

        info("Waiting: Server not ready")
        self.k8.wait_for_resource(deployment, "Deployment")
        iperf3_server = {"meta": {"name": "iperf3-server"}}
        self.k8.wait_for_resource(iperf3_server, "Service")
        sleep(1)

    def deploy_client(self, client_node):
        configs = yaml.load_to_dicts("benchmarks/bandwidth/iperf3-client.yaml")
        job = configs[0]
        nodeSelector = {"kubernetes.io/hostname": client_node}
        job["spec"]["template"]["spec"]["nodeSelector"] = nodeSelector
        if self.k8.exists_in_kubernetes(job, "Job"):
            self.k8.delete_job(job)
            debug("Job already exists, deleting it")
        # Create job
        sleep(2)
        info("Creating client benchmark job")
        self.k8.create_from_dict(job)
        debug(f"Job `{job['metadata']['name']}` created.")

        return self.k8.get_job_logs(job)

    def cleanup(self):
        deployment, service = self.server_resources
        if self.k8.exists_in_kubernetes(deployment, "Deployment"):
            self.k8.delete_deployment(deployment)
            self.k8.wait_for_deletion(deployment, "Deployment")
        if self.k8.exists_in_kubernetes(service, "Service"):
            self.k8.delete_service(service)
            self.k8.wait_for_deletion(service, "Service")

        job = self.client_resources[0]
        if self.k8.exists_in_kubernetes(job, "Job"):
            self.k8.delete_job(job)
            self.k8.wait_for_deletion(job, "Job")
