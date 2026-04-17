import csv
from simulation import simulate
from graphs import plot_results

traffic_levels = ["low", "medium", "high"]

delays = []
throughputs = []
losses = []

# Create CSV file
with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Traffic", "Delay", "Throughput", "Packet Loss %"])

    for level in traffic_levels:
        print(f"\nRunning {level.upper()} traffic...")
        d, t, l = simulate(level)

        delays.append(d)
        throughputs.append(t)
        losses.append(l)

        writer.writerow([level, d, t, l])

# Plot graphs
plot_results(delays, throughputs, losses)

# Save summary report
with open("report.txt", "w") as f:
    for i, level in enumerate(traffic_levels):
        f.write(f"{level.upper()} Traffic:\n")
        f.write(f"Delay: {delays[i]:.4f}\n")
        f.write(f"Throughput: {throughputs[i]:.2f}\n")
        f.write(f"Packet Loss %: {losses[i]:.2f}\n\n")

print("\n✅ Results saved to results.csv and report.txt")