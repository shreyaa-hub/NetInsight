import matplotlib.pyplot as plt
import csv

def show_graphs(dark_mode=False):
    traffic = []
    delays = []
    throughputs = []
    losses = []

    try:
        with open("results.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                traffic.append(row["Traffic"].capitalize())
                delays.append(float(row["Delay"]) * 1000)  # ms
                throughputs.append(float(row["Throughput"]))
                losses.append(float(row["Packet Loss %"]))

    except FileNotFoundError:
        print("⚠️ Run simulation first to generate results.csv")
        return

    # 🎨 Theme setup
    if dark_mode:
        plt.style.use("dark_background")
        bar_colors = ["#4cc9f0", "#f72585", "#b5179e"]
        text_color = "white"
    else:
        plt.style.use("default")
        bar_colors = ["#4361ee", "#2a9d8f", "#e76f51"]
        text_color = "black"

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    def add_labels(ax, values):
        for i, v in enumerate(values):
            ax.text(i, v, f"{v:.2f}", ha='center', va='bottom', color=text_color, fontsize=10)

    # 🔹 Delay
    axs[0].bar(traffic, delays, color=bar_colors[0], edgecolor='black')
    axs[0].set_title("Delay", color=text_color, fontsize=13)
    axs[0].set_xlabel("Traffic", color=text_color)
    axs[0].set_ylabel("Delay (ms)", color=text_color)
    axs[0].ticklabel_format(style='plain', axis='y')
    add_labels(axs[0], delays)

    # 🔹 Throughput
    axs[1].bar(traffic, throughputs, color=bar_colors[1], edgecolor='black')
    axs[1].set_title("Throughput", color=text_color, fontsize=13)
    axs[1].set_xlabel("Traffic", color=text_color)
    add_labels(axs[1], throughputs)

    # 🔹 Packet Loss
    axs[2].bar(traffic, losses, color=bar_colors[2], edgecolor='black')
    axs[2].set_title("Packet Loss %", color=text_color, fontsize=13)
    axs[2].set_xlabel("Traffic", color=text_color)
    add_labels(axs[2], losses)

    # Clean spacing
    plt.subplots_adjust(wspace=0.35)
    plt.tight_layout()

    # Save images (both versions)
    filename = "network_performance_dark.png" if dark_mode else "network_performance_light.png"
    plt.savefig(filename, dpi=300)

    print(f"📸 Graph saved as '{filename}'")

    plt.show()