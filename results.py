import csv
from simulation import simulate
from graphs import show_graphs

def run_simulation():
    traffic_levels = ["low", "medium", "high"]
    results = []

    print("\n===== RUNNING NETWORK SIMULATION =====\n")

    for level in traffic_levels:
        print(f"Running {level.upper()} traffic...")

        delay, throughput, loss = simulate(level)
        results.append((level, delay, throughput, loss))

        print(f"Delay: {delay:.4f}")
        print(f"Throughput: {throughput:.2f}")
        print(f"Packet Loss %: {loss:.2f}\n")

    # Save CSV
    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Traffic", "Delay", "Throughput", "Packet Loss %"])
        for row in results:
            writer.writerow(row)

    # Save Report
    with open("report.txt", "w") as f:
        for level, delay, throughput, loss in results:
            f.write(f"{level.upper()} Traffic:\n")
            f.write(f"Delay: {delay:.4f}\n")
            f.write(f"Throughput: {throughput:.2f}\n")
            f.write(f"Packet Loss %: {loss:.2f}\n\n")

    print("✅ Simulation complete and results saved!\n")


def view_results():
    try:
        print("\n===== SAVED RESULTS =====\n")
        with open("report.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("⚠️ No results found. Run simulation first.\n")


def main_menu():
    while True:
        print("===== NetInsight System =====")
        print("1. Run Simulation")
        print("2. View Results")
        print("3. Show Graphs")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_simulation()
        elif choice == "2":
            view_results()
        elif choice == "3":
            show_graphs()
        elif choice == "4":
            print("Exiting... 👋")
            break
        else:
            print("Invalid choice. Try again.\n")


# Start program
main_menu()