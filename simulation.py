import time
import random
import numpy as np
from metrics import calculate_metrics

def generate_packets(level):
    if level == "low":
        return np.random.poisson(lam=2)
    elif level == "medium":
        return np.random.poisson(lam=4)
    elif level == "high":
        return np.random.poisson(lam=7)

def simulate(traffic_level, cycles=30, queue_size=10, process_rate=2, use_priority=True):

    queue = []

    total_packets = 0
    dropped_packets = 0
    processed_packets = 0
    total_delay = 0

    delays = []  # for jitter

    for cycle in range(cycles):

        new_packets = generate_packets(traffic_level)

        for _ in range(new_packets):
            total_packets += 1

            # 🔥 Packet Priority (QoS)
            priority = random.choice(["high", "low"])

            packet = {
                "arrival": time.time(),
                "priority": priority
            }

            if len(queue) < queue_size:
                queue.append(packet)
            else:
                dropped_packets += 1

        # 🔥 PRIORITY QUEUE (high first)
        if use_priority:
            queue.sort(key=lambda x: x["priority"] != "high")

        for _ in range(process_rate):
            if queue:
                packet = queue.pop(0)

                delay = time.time() - packet["arrival"]
                total_delay += delay
                processed_packets += 1
                delays.append(delay)

    # 🔥 JITTER calculation
    jitter = 0
    if len(delays) > 1:
        jitter = sum(abs(delays[i] - delays[i-1]) for i in range(1, len(delays))) / (len(delays)-1)

    avg_delay, throughput, loss_percent = calculate_metrics(
        total_packets,
        processed_packets,
        dropped_packets,
        total_delay,
        cycles
    )

    return avg_delay, throughput, loss_percent, jitter