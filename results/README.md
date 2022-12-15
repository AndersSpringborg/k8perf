# Results
This directory contains the results of the experiments on network metrics in different regions in AWS and Azure.

The results are stored in the following format:
- `images` contains heatmaps of the network metrics: `latency`, `RTT`, `bandwidth`, `retransmisisons`, `cpu usage`.
    Each folder represent a VM type in AWS or Azure, and the heatmaps have this type of vm deployed in different regions.
    
    An example is: `m5.large/rtt.png` shows round trip time for US West 1,2,3 and 4, on m5.large instances.
- `results` contains the raw data of the network metrics.

## Virtual Machines
The following VMs were used in the experiments:

| VM Type   | vCPU | Memory | Network Bandwidth | Price (USD) |
|-----------|------|--------|-------------------|-------------|
| m5.large  | 2    | 8 GB   | 10 Gbps           | 0.096       |
| m5.xlarge | 4    | 16 GB  | 10 Gbps           | 0.192       |
| c5n.large | 2    | 5 GB   | 10 Gbps           | 0.096       |


Instance vCPU Memory Bandwidth
t2.micro 1 1 GB Low to Moderate
t3.micro 2 1 GB Up to 5Gb
m5.large 2 8 GB Up to 10Gb
c5n.large 2 5.25 GB Up to 25Gb
D4ds_v4 4 16.0 Up to 10Gb
Table 1: Instance types for AWS experiments

| VM Type   | vCPU |  Memory | Network Bandwidth | Price (USD) | Cloud Provider |
|-----------|------|--------:|-------------------|-------------|----------------|
| t2.micro  | 1    |  1.0 GB | Low to Moderate   | 0.0116      | 🟧️ AWS        |
| t3.micro  | 2    |  1.0 GB | Up to 5Gb         | 0.0104      | 🟧 AWS         |
| m5.large  | 2    |  8.0 GB | Up to 10Gb        | 0.096       | 🟧 AWS         |
| c5n.large | 2    |  5.3 GB | Up to 25Gb        | 0.1080      | 🟧 AWS         |
| D4ds_v4   | 4    | 16.0 GB | Up to 10Gb        | 0.192       | 🟦 Azure       |



