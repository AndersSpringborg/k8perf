import json
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, Literal
import matplotlib.pyplot as plt

import seaborn as sns
import pandas as pandas
import typer
from kubernetes import config
from kubernetes.client import V1NodeList, V1Node
from kubernetes.config import ConfigException
from rich.pretty import pprint
from rich import print
from setuptools_scm import get_version

from k8perf.benchmark import BenchmarkRunner
from k8perf.benchmarks import IPerfBenchmark
from k8perf.util_terminal_ui import terminal_menu, show_result, bytes_to_human_readable
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging
from rich.logging import RichHandler

app = typer.Typer(help="Benchmark runner for network benchmarks.")

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


@app.callback()
def main(version: bool = False):
    if version:
        print(f"k8perf CLI Version: {get_version()}")
        raise typer.Exit()


def parse_benchmark_json(benchmark_json: Dict) -> (float, float, float):
    """Parse benchmark json to get mbps and cpu usage."""
    bps = benchmark_json["end"]["sum_received"]["bits_per_second"]
    cpu_host = float(benchmark_json["end"]["cpu_utilization_percent"]["host_total"])
    cpu_client = float(benchmark_json["end"]["cpu_utilization_percent"]["host_total"])
    mean_rtt = float(benchmark_json["end"]["streams"][0]["sender"]["mean_rtt"])
    retransmits = int(benchmark_json["end"]["streams"][0]["sender"]["retransmits"])

    return bps, cpu_host, cpu_client, mean_rtt, retransmits


def benchmark_all_nodes(nodes: V1NodeList.items):
    """Benchmark all nodes in the cluster."""
    benchmark_pd = pandas.DataFrame()
    json_results = []
    node_names = [node.metadata.name for node in nodes]
    for client_node in node_names:
        for server_node in node_names:
            benchmark = IPerfBenchmark(client_node=client_node, server_node=server_node)
            benchmark_json = benchmark.run()
            json_results.append(benchmark_json)
            mbps, cpu_host, cpu_client, mean_rtt, retransmits = parse_benchmark_json(benchmark_json)
            benchmark_pd = benchmark_pd.append(
                {
                    "client_node": client_node,
                    "server_node": server_node,
                    "mbps": mbps,
                    "cpu_host": cpu_host,
                    "cpu_client": cpu_client,
                    "mean_rtt": mean_rtt,
                    "retransmits": retransmits
                },
                ignore_index=True,
            )
    print(benchmark_pd)
    benchmark_pd.to_csv("benchmark.csv")
    with open("benchmark.json", "w") as f:
        f.write(str(json_results))


def find_kubernetes_config():
    """Find kubernetes config."""
    try:
        config.load_kube_config()
    except ConfigException as e:
        logging.error(f"Could not load kube config: {e}")
        raise typer.Abort()


@app.command()
def run(delete_pods: bool = True, debug: bool = False, json: bool = False, all_nodes: bool = False,
        plot: bool = False, csv: str = None):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    from kubernetes import client
    find_kubernetes_config()

    k8s_api = client.CoreV1Api()
    # nodes = [(node, 1) for node in k8s_api.list_node().items]
    # get nodes that do not have "noSchedule" taint
    nodes = [node for node in k8s_api.list_node().items if not node.spec.taints]

    if all_nodes:
        benchmark_all_nodes(nodes)
        raise typer.Exit()

    node_names = [node.metadata.name for node in nodes]
    # remove from memory
    nodes = None

    server_nodes = terminal_menu("Choose a server to run on:", node_names)
    client_nodes = terminal_menu("Choose a client to run on:", node_names)
    # remove from memory
    node_names = None
    if "None" in client_nodes or "None" in server_nodes:
        typer.echo("Exiting...")
        raise typer.Exit()

    if any(node in server_nodes for node in client_nodes):
        typer.echo("FIY: You have a benchmark running both as a client and server on the same node")
    confirm = input("Do you wanna deploy on these nodes? [y/n] ")
    if confirm.lower() != "y":
        raise typer.Exit()

    # loading animation
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        task = progress.add_task("Running benchmark...", total=1)
        runner = BenchmarkRunner(client_node_names=client_nodes, server_node_names=server_nodes)
        runner.run()
        progress.update(task, advance=1, description="Cleaning up...")
        if delete_pods:
            runner.cleanup()

    if json:
        pprint(runner.json())
    else:
        pprint(runner.benchmark_results)

    if csv is not None:
        runner.benchmark_results.results.to_csv(csv)

    if plot:
        typer.echo("plot")

    typer.echo("Done!")


def merge_two_columns_to_one(df: pandas.DataFrame, column1: str, column2: str):
    df[column1] = df[column1].fillna(df[column2])
    return df


def replace_own_values(rtt, own, new_node):
    rtt[own][own] = rtt[own][new_node]
    return rtt.drop(new_node)


def rename_df_columns_and_roows(rtt, renaming):
    """
    Exmaple:
    renaming = {
        "aks-az1-52939702-vmss000000": "US West AZ-1",
        "aks-az2-26374771-vmss000000": "US East AZ-2",
        "aks-az3-17689621-vmss000000": "US West AZ-3"}
    :param rtt:
    :param renaming:
    :return:
    """
    rtt = rtt.rename(columns=renaming)
    rtt = rtt.rename(index=renaming)
    return rtt


def make_image(df, value, json_key, title, directory, vmin=None, vmax=None, fmt=".2f"):
    logging.info(f"Making image for {json_key}")
    try:
        rtt = df.pivot(index="client_node", columns="server_node", values=json_key)
    except KeyError:
        logging.error(f"Could not find {json_key} in dataframe")
        return

    sns.heatmap(rtt, annot=True, annot_kws={"size": 17}, fmt=fmt, vmin=vmin, vmax=vmax)
    plt.title("D4s_v4 " + title, fontsize=20)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(directory + value + ".png", dpi=150, bbox_inches="tight")
    plt.show()


class PlotMetrics(str, Enum):
    rtt = "rtt"
    mbps = "mbps"
    cpu_server = "cpu_host"
    cpu_client = "cpu_client"
    retransmits = "retransmits"
    httpAverageResponseTime = "httpAverageResponseTime"
    all = "all"


class PlotMetricsFrontend(str, Enum):
    rtt = "rtt"
    mbps = "mbps"
    cpu_host = "cpu-s"
    cpu_client = "cpu-c"
    retransmits = "retrans"
    httpAverageResponseTime = "http"
    all = "all"

    def map(self):
        mapping = {
            "rtt": PlotMetrics.rtt,
            "mbps": PlotMetrics.mbps,
            "cpu-s": PlotMetrics.cpu_server,
            "cpu-c": PlotMetrics.cpu_client,
            "retrans": PlotMetrics.retransmits,
            "http": PlotMetrics.httpAverageResponseTime,
            "all": PlotMetrics.all,

        }
        return mapping[self._value_]


@app.command()
def heatmap(csv_file_path: Path, image_output_directory: Path, metric: PlotMetricsFrontend = PlotMetricsFrontend.all):
    if not csv_file_path.exists():
        typer.echo("File does not exist")
        raise typer.Abort()
    if not csv_file_path.suffix == ".csv":
        print("[yellow]File is not a csv file[/yellow]")
        if not typer.confirm("Do you want to continue?"):
            raise typer.Abort()
    if not image_output_directory.exists():
        typer.echo("Directory does not exist, creating it")
        image_output_directory.mkdir(parents=True)
    if not image_output_directory.is_dir():
        typer.echo("Path is not a directory")
        raise typer.Abort()
    metric = metric.map()

    df = pandas.read_csv(csv_file_path)
    client_nodes = df["client_node"].unique()
    server_nodes = df["server_node"].unique()
    server_and_client_nodes_names = server_nodes.tolist() + client_nodes.tolist()
    # find uniques and sort them
    server_and_client_nodes_names = list(set(server_and_client_nodes_names))
    # server_and_client_nodes_names.sort()
    logging.debug("All plotting nodes: ", server_and_client_nodes_names)
    all_metrics = metric == "all"
    if all_metrics:
        logging.info("Plotting all metrics")

    path = image_output_directory.as_posix() + "/"
    if all_metrics or metric == "rtt":
        # divide mean rtt with 1000 for ms
        df["mean_rtt"] = df["mean_rtt"] / 1000
        make_image(df, "rtt", "mean_rtt", "RTT in ms", path, fmt=".1f")
    if all_metrics or metric == "mbps":
        df["mbps"] = df["mbps"] / 1000
        make_image(df, "mbps", "mbps", "Throughput in Gbps", path)
    if all_metrics or metric == "cpu_host":
        make_image(df, "cpu_host", "cpu_host", "CPU Host %", path, fmt=".1f")
    if all_metrics or metric == "cpu_client":
        make_image(df, "cpu_client", "cpu_client", "CPU Client %", path, fmt=".1f")
    if all_metrics or metric == "retransmits":
        make_image(df, "retransmits", "retransmits", "Retransmits", path, fmt=".0f")
    if all_metrics or metric == "httpAverageResponseTime":
        make_image(df, "httpAverageResponseTime", "httpAverageResponseTime", "HTTP Average Response Time", path,
                   fmt=".1f")


if __name__ == "__main__":
    app()

# https://www.cockroachlabs.com/blog/cockroachdb-kubernetes-cilium/
