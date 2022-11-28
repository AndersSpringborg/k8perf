from logging import info, debug
from os import path
from time import sleep

from . import util_yaml as yaml
from .kubernetes_integration import KubernetesIntegration

BENCHMARK_NAMESPACE = "network-benchmarks"


class IPerfBenchmark:
    def __init__(self, client_node, server_node):
        self.client_node = client_node
        self.server_node = server_node
        self.k8 = KubernetesIntegration(namespace="default")
    def run(self):
        return self.iperf3_benchmark_kubernetes(self.client_node, self.server_node)

    def iperf3_benchmark_kubernetes(self, client_node, server_node):

        info("Running iperf3 benchmark on Kubernetes")

        self.deploy_server(server_node)

        # Wait for server to be ready
        info("Waiting: Server not ready")
        iperf3_server = {"meta": {"name": "iperf3-server"}}
        self.k8.wait_for_resource(iperf3_server, "Service")
        return self.deploy_client(client_node)

    def deploy_server(self, server_node):
        configs = yaml.load_to_dicts("bandwidth/iperf3-server.yaml")
        deployment, service = configs
        nodeSelector = {"kubernetes.io/hostname": server_node}
        deployment["spec"]["template"]["spec"]["nodeSelector"] = nodeSelector
        if self.k8.exists_in_kubernetes(deployment, "Deployment"):
            self.k8.delete_deployment(deployment)
            self.k8.wait_for_deletion(deployment, "Deployment")
        if self.k8.exists_in_kubernetes(service, "Service"):
            self.k8.delete_service(service)
            self.k8.wait_for_deletion(service, "Service")
        # Create deployment
        # self.wait_for_resource(service, "Service")
        info ("Creating server deployment")
        self.k8.create_from_dict(deployment)
        info("Creating server service")
        self.k8.create_from_dict(service)

    def deploy_client(self, client_node):
        configs = yaml.load_to_dicts("bandwidth/iperf3-client.yaml")
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

        # Wait for job to finish
        self.k8.wait_for_resource(job, "Job")

        # Get logs from job
        debug("Getting logs from job")
        return self.k8.get_job_logs(job)
