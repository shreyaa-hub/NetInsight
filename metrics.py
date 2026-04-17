# metrics.py

def calculate_metrics(total_packets, processed_packets, dropped_packets, total_delay, cycles):
    
    # Average Delay
    avg_delay = total_delay / processed_packets if processed_packets else 0

    # Throughput
    throughput = processed_packets / cycles

    # Packet Loss %
    loss_percent = (dropped_packets / total_packets) * 100 if total_packets else 0

    return avg_delay, throughput, loss_percent