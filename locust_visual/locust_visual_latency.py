import matplotlib.pyplot as plt


title = "Average Latency (ms) vs. # of users per second"
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
ylabel = "Average Latency (ms)"

# data extracted from data/experiment 2/... from locust branch
latency = [
    [3, 3, 10, 114, 519],
    [2, 3, 6, 74, 415],
    [1, 2, 5, 79, 415],
    [2, 3, 4, 21, 288],
    [2, 3, 5, 27, 284],
    [2, 3, 5, 19, 284],
    [1, 1, 2, 8, 224],
    [1, 1, 2, 7, 220],
    [1, 1, 2, 6, 212]
]


# Draw the plot of average latency
plt.figure(figsize=(12, 8))
for index, y in enumerate(latency):
    plt.plot(x, y, label=labels[index], marker='o', linewidth=2)
plt.title(title, fontsize=18)
plt.xticks(x, x_ticks, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="upper left", fontsize=16)
plt.xlabel(xlabel, fontsize=16)
plt.ylabel(ylabel, fontsize=16)
plt.savefig("images/locust/locust_latency.png", dpi=150, bbox_inches="tight")
plt.show()