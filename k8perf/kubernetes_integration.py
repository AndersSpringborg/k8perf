import json
from logging import info, debug
from time import sleep
from typing import Literal, Callable

from kubernetes import dynamic, config, client, utils
from kubernetes.client import api_client, ApiException, V1Pod, V1PodStatus, V1PodCondition
from kubernetes.dynamic.exceptions import NotFoundError

RESOURCE_TYPES = Literal["Job", "Service", "Deployment"]


class KubernetesIntegration:
    def __init__(self, namespace="default"):
        self.namespace = namespace
        self.client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_kube_config())
        )
        self.apps_v1 = client.AppsV1Api()
        self.batch_v1 = client.BatchV1Api()
        self.core_v1 = client.CoreV1Api()
        self.api = client.ApiClient()

    def wait_for_resource(self, kube_resource, resource_type: RESOURCE_TYPES):
        name = ""
        if "metadata" in kube_resource.keys():
            name = kube_resource["metadata"]["name"]
        elif "meta" in kube_resource.keys():
            name = kube_resource["meta"]["name"]
        else:
            raise Exception("Resource name is empty")

        if resource_type == "Deployment":
            while True:
                resp = self.apps_v1.read_namespaced_deployment_status(
                    name=name, namespace=self.namespace
                )
                if resp.status.ready_replicas == resp.status.replicas:
                    break
                else:
                    info(f"Waiting: Deployment not ready `{name}`")
                    sleep(2)
        elif resource_type == "Job":
            timer = 0
            info(f"Waiting: Job not finished `{name}`")
            while timer < 120:
                resp = self.batch_v1.read_namespaced_job_status(
                    name=name, namespace=self.namespace
                )
                if resp.status.succeeded == 1:
                    info("Job finished")
                    return
                else:
                    sleep(2)
                    timer += 2
            raise TimeoutError("Job timed out")
        elif resource_type == "Service":
            while True:
                try:
                    resp = self.core_v1.read_namespaced_service_status(
                        name=name, namespace=self.namespace
                    )
                    break
                except NotFoundError as e:
                    info(f"Waiting: Service not ready `{name}`")
                    sleep(2)

        else:
            raise Exception("Resource type not supported")

    def delete_deployment(self, kube_resource, namespace="default"):
        # Delete deployment
        resp = self.apps_v1.delete_namespaced_deployment(
            name=kube_resource["metadata"]["name"],
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground", grace_period_seconds=5
            ),
        )

    def delete_job(self, kube_resource, namespace="default"):
        # Delete job
        resp = self.batch_v1.delete_namespaced_job(
            name=kube_resource["metadata"]["name"],
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground", grace_period_seconds=5
            ),
        )

        debug(f"Job `{kube_resource['metadata']['name']}` deleted.")

    def delete_service(self, kube_resource, namespace="default"):
        # Delete service
        resp = self.core_v1.delete_namespaced_service(
            name=kube_resource["metadata"]["name"],
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy="Foreground", grace_period_seconds=5
            ),
        )

    def get_job_logs(self, kube_resource):
        debug(f"Getting logs from job `{kube_resource}`")
        # wait for job to finish
        self.wait_for_resource(kube_resource, "Job")

        # get pod with job selector
        from kubernetes.client import V1PodList
        pod_selector = f"job-name={kube_resource['metadata']['name']}"
        api_response: V1PodList = self.core_v1.list_namespaced_pod(
            namespace=self.namespace, label_selector=pod_selector
        )

        # select pod with status condition reason PodCompleted
        def find_completed_pod(pod: V1Pod) -> bool:
            status: V1PodStatus = pod.status
            condition: V1PodCondition = status.conditions[2]
            return condition.reason == "PodCompleted"
        job_pod_name = list(filter(find_completed_pod, api_response.items))[0].metadata.name

        # get logs from pod
        pod_log = self.core_v1.read_namespaced_pod_log(
            name=job_pod_name, namespace=self.namespace
        )

        pod_log_json = (
            pod_log.replace("'", '"').replace("True", "true").replace("False", "false")
        )

        benchmark_result = json.loads(pod_log_json)
        return benchmark_result

    def exists_in_kubernetes(
            self, resource, resource_type: RESOURCE_TYPES, name=""
    ) -> bool:
        if type(resource) is dict and "metadata" in resource.keys():
            name = resource["metadata"]["name"]

        if name == "":
            raise Exception("Resource name is empty")

        lookup_function = getattr(
            self.client.resources.get(api_version="v1", kind=resource_type), "get"
        )

        try:
            lookup_function(name=name, namespace="default")
            return True
        except ApiException as e:
            if e.status == 404:
                return False
            raise e

    def create_from_dict(self, deployment):
        utils.create_from_dict(self.api, deployment, namespace=self.namespace)

    def wait_for_deletion(self, resource, resource_type: RESOURCE_TYPES, name=""):
        if type(resource) is dict and "metadata" in resource.keys():
            name = resource["metadata"]["name"]

        if name == "":
            raise Exception("Resource name is empty")

        lookup_function = getattr(
            self.client.resources.get(api_version="v1", kind=resource_type), "get"
        )

        while True:
            try:
                lookup_function(name=name, namespace="default")
                sleep(2)
            except ApiException as e:
                if e.status == 404:
                    break
                raise e
