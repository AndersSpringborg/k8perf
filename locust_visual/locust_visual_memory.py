import matplotlib.pyplot as plt


client_title = "Memory usage rate (%) of Client Application"
server_title = "Memory usage rate (%) of Server Application"
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
ylabel = "Memory usage rate (%)"

# data extracted from data/experiment 2/... from locust branch
mem_client = [
    [80, 80, 81, 82, 80],
    [68, 73, 74, 78, 82],
    [68, 76, 80, 81, 84],
    [80, 79, 79, 81, 77],
    [84, 84, 84, 82, 77],
    [78, 78, 77, 78, 75],
    [12, 12, 13, 14, 14],
    [13, 13, 13, 13, 13],
    [12, 13, 13, 13, 14]
]

mem_server = [
    [76, 76, 76, 76, 71],
    [75, 77, 71, 70, 69],
    [12, 12, 12, 12, 12],
    [72, 72, 72, 72, 77],
    [75, 75, 74, 74, 69],
    [12, 12, 12, 12, 12],
    [70, 72, 72, 73, 73],
    [75, 75, 75, 75, 73],
    [12, 12, 12, 12, 12]
]


# Draw the plot of Client Memory
plt.figure(figsize=(12, 8))
for index, y in enumerate(mem_client):
    plt.plot(x, y, label=labels[index], marker='o', linewidth=2)
plt.title(client_title, fontsize=18)
plt.xticks(x, x_ticks, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="lower right", fontsize=16)
plt.xlabel(xlabel, fontsize=16)
plt.ylabel(ylabel, fontsize=16)
plt.savefig("images/locust/mem_client.png", dpi=150, bbox_inches="tight")
plt.show()

# Draw the plot of Server Memory
plt.figure(figsize=(12, 8))
for index, y in enumerate(mem_server):
    plt.plot(x, y, label=labels[index], marker='o', linewidth=2)
plt.title(server_title, fontsize=18)
plt.xticks(x, x_ticks, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="upper left", fontsize=16)
plt.xlabel(xlabel, fontsize=16)
plt.ylabel(ylabel, fontsize=16)
plt.savefig("images/locust/mem_server.png", dpi=150, bbox_inches="tight")
plt.show()