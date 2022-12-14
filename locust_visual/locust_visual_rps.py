import matplotlib.pyplot as plt


title = "Request per second vs. # of users per second"
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
ylabel = "Request per second"

# data extracted from data/experiment 2/... from locust branch
rps = [
    [65.07, 323.14, 616.91, 698.85, 654.56],
    [65.62, 324.82, 632.37, 832.44, 777.87],
    [65.64, 325.07, 635.57, 813.22, 777.59],
    [65.51, 324.25, 641.25, 1135.68, 1022.61],
    [65.10, 323.10, 637.30, 1085.44, 1033.00],
    [65.12, 324.53, 639.56, 1149.84, 1034.88],
    [65.92, 328.77, 654.23, 1250.00, 1215.31],
    [65.81, 328.78, 655.34, 1258.94, 1231.41],
    [65.81, 328.79, 654.26, 1264.27, 1259.53]
]


# Draw the plot of Client CPU
plt.figure(figsize=(12, 8))
for index, y in enumerate(rps):
    plt.plot(x, y, label=labels[index], marker='o', linewidth=2)
plt.title(title, fontsize=18)
plt.xticks(x, x_ticks, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="upper left", fontsize=16)
plt.xlabel(xlabel, fontsize=16)
plt.ylabel(ylabel, fontsize=16)
plt.savefig("images/locust/locust_rps.png", dpi=150, bbox_inches="tight")
plt.show()