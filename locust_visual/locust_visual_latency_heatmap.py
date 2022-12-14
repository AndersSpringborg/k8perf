import seaborn as sns
import matplotlib.pyplot as plt


title = "Latency (ms)"
axis_label = ["t2.micro", "t3.micro", "c5n.large"]
ylabel = "Client Instance Type"
xlabel = "Server Instance Type"

# Experiment data of locust
# Check data folder under "locust" branch
u10r10 = [
    [8, 6, 6],
    [8, 13, 8],
    [3, 5, 3]
]

u50r50 = [
    [25, 13, 77],
    [14, 43, 13],
    [5, 5, 4]
]

u100r100 = [
    [50, 86, 41],
    [42, 160, 59],
    [7, 7, 6]
]

u200r200 = [
    [190, 200, 210],
    [79, 210, 110],
    [35, 30, 34]
]

u500r500 = [
    [630, 580, 630],
    [520, 450, 460],
    [350, 350, 350]
]


# u10r10
sns.heatmap(u10r10, annot=u10r10, xticklabels=axis_label, yticklabels=axis_label,
            annot_kws={"size":17}, fmt=".20g")
plt.title(title, fontsize=20)
plt.xlabel(xlabel, fontsize=17)
plt.ylabel(ylabel, fontsize=17)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.savefig("images/locust/u10r10.png", dpi=150, bbox_inches="tight")
plt.show()

# u50r50
sns.heatmap(u50r50, annot=u50r50, xticklabels=axis_label, yticklabels=axis_label,
            annot_kws={"size":17}, fmt=".20g")
plt.title(title, fontsize=20)
plt.xlabel(xlabel, fontsize=17)
plt.ylabel(ylabel, fontsize=17)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.savefig("images/locust/u50r50.png", dpi=150, bbox_inches="tight")
plt.show()

# u100r100
sns.heatmap(u100r100, annot=u100r100, xticklabels=axis_label, yticklabels=axis_label,
            annot_kws={"size":17}, fmt=".20g")
plt.title(title, fontsize=20)
plt.xlabel(xlabel, fontsize=17)
plt.ylabel(ylabel, fontsize=17)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.savefig("images/locust/u100r100.png", dpi=150, bbox_inches="tight")
plt.show()

# u200r200
sns.heatmap(u200r200, annot=u200r200, xticklabels=axis_label, yticklabels=axis_label,
            annot_kws={"size":17}, fmt=".20g")
plt.title(title, fontsize=20)
plt.xlabel(xlabel, fontsize=17)
plt.ylabel(ylabel, fontsize=17)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.savefig("images/locust/u200r200.png", dpi=150, bbox_inches="tight")
plt.show()

# u500r500
sns.heatmap(u500r500, annot=u500r500, xticklabels=axis_label, yticklabels=axis_label,
            annot_kws={"size":17}, fmt=".20g")
plt.title(title, fontsize=20)
plt.xlabel(xlabel, fontsize=17)
plt.ylabel(ylabel, fontsize=17)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.savefig("images/locust/u500r500.png", dpi=150, bbox_inches="tight")
plt.show()