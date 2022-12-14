import matplotlib.pyplot as plt


client_title = "CPU usage rate (%) of Client Application"
server_title = "CPU usage rate (%) of Server Application"
labels = [
    "t2.micro to t2.micro",
    "t2.micro to t3.micro",
    "t2.micro to c5n.large",
    "t3.micro to t2.micro",
    "t3.micro to t3.micro",
    "t3.micro to c5n.large",
    "c5n.large to t2.micro",
    "c5n.large to t3.micro",
    "c5n.large to c5n.large"
]

x = [1, 2, 3, 4, 5]
x_ticks = ["10", "50", "100", "200", "500"]
xlabel = "Number of users per second"
ylabel = "CPU usage rate (%)"

# data extracted from data/experiment 2/... from locust branch
cpu_client = [
    [16.3, 55.3, 85.7, 98.1, 99.5],
    [12.6, 42.6, 78.6, 97.7, 97.2],
    [13.3, 46.8, 78.7, 97.3, 97.3],
    [13.4, 38.7, 68.7, 102.7, 98.6],
    [13.6, 39.2, 66.2, 102.9, 98.8],
    [16.2, 44.7, 64.1, 102.3, 98.7],
    [9.4, 32.3, 56.3, 99.6, 97.9],
    [18.3, 29.2, 54.6, 98.2, 97.3],
    [8.5, 29.6, 54.6, 97.8, 97.5]
]

cpu_server = [
    [4.8, 7.4, 15.6, 17.1, 21.7],
    [3, 5.7, 8.3, 9.7, 9],
    [2, 4.4, 6.6, 8.1, 8],
    [5.8, 10.6, 16.2, 25, 22.9],
    [3.1, 5.8, 8.1, 12.5, 11.6],
    [2.1, 3.8, 7.2, 10.8, 10.2],
    [5.3, 5.9, 16.4, 25.2, 16.6],
    [3.1, 6, 8.3, 13, 14],
    [2.1, 4.2, 6, 11, 12]
]


# Draw the plot of Client CPU
plt.figure(figsize=(12, 8))
for index, y in enumerate(cpu_client):
    plt.plot(x, y, label=labels[index], marker='o', linewidth=2)
plt.title(client_title, fontsize=18)
plt.xticks(x, x_ticks, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="lower right", fontsize=16)
plt.xlabel(xlabel, fontsize=16)
plt.ylabel(ylabel, fontsize=16)
plt.savefig("images/locust/cpu_client.png", dpi=150, bbox_inches="tight")
plt.show()

# Draw the plot of Server CPU
plt.figure(figsize=(12, 8))
for index, y in enumerate(cpu_server):
    plt.plot(x, y, label=labels[index], marker='o', linewidth=2)
plt.title(server_title, fontsize=18)
plt.xticks(x, x_ticks, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="upper left", fontsize=16)
plt.xlabel(xlabel, fontsize=16)
plt.ylabel(ylabel, fontsize=16)
plt.savefig("images/locust/cpu_server.png", dpi=150, bbox_inches="tight")
plt.show()