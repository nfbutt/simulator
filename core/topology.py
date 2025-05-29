import math

class Topology:
    def __init__(self, config):
        self.config = config


class RingTopology(Topology):
    def simulate_allreduce(self, gpus, size_gb):
        """
        Simulate Ring-Based AllReduce:
        - Reduce-Scatter: Each GPU sends/receives n-1 chunks
        - All-Gather: Each GPU receives n-1 chunks
        Total: 2(n-1) steps
        """
        n = len(gpus)
        chunk_per_gpu = size_gb / n
        chunk_size_gb = self.config.chunk_size / (1024 ** 3)
        steps = int(chunk_per_gpu / chunk_size_gb)

        # 2(n-1) steps in Ring AllReduce
        for step in range(2 * (n - 1)):
            for i in range(n):
                sender = gpus[i]
                receiver = gpus[(i + 1) % n]
                # Effective bandwidth = min(sender_bw, receiver_bw)
                bandwidth = min(sender.config.bandwidth, receiver.config.bandwidth)
                duration = chunk_size_gb / bandwidth  # communication overhead per chunk

                # Synchronize sender/receiver before transfer
                start_time = max(sender.clock, receiver.clock)
                sender.wait_until(start_time)
                receiver.wait_until(start_time)
                sender.execute_comm(duration)
                receiver.execute_comm(duration)


class TreeTopology(Topology):
    def simulate_allreduce(self, gpus, size_gb):
        """
        Simulate Tree-Based AllReduce:
        - Reduction Phase: log2(N) steps
        - Broadcast Phase: log2(N) steps
        """
        levels = int(math.ceil(math.log2(len(gpus))))
        chunk_size_gb = self.config.chunk_size / (1024 ** 3)
        duration = chunk_size_gb / min(g.config.bandwidth for g in gpus)

        # Reduction (up the tree)
        for level in range(levels):
            step = 2 ** level
            for i in range(0, len(gpus), step * 2):
                if i + step < len(gpus):
                    g1, g2 = gpus[i], gpus[i + step]
                    t = max(g1.clock, g2.clock)
                    g1.wait_until(t)
                    g2.wait_until(t)
                    g1.execute_comm(duration)
                    g2.execute_comm(duration)

        # Broadcast (down the tree)
        for level in reversed(range(levels)):
            step = 2 ** level
            for i in range(0, len(gpus), step * 2):
                if i + step < len(gpus):
                    g1, g2 = gpus[i], gpus[i + step]
                    t = max(g1.clock, g2.clock)
                    g1.wait_until(t)
                    g2.wait_until(t)
                    g1.execute_comm(duration)
                    g2.execute_comm(duration)


class FullyConnectedTopology(Topology):
    def simulate_allreduce(self, gpus, size_gb):
        """
        Simulate Fully Connected AllReduce:
        - Each GPU communicates with every other GPU
        - Leads to O(N^2) communication
        """
        n = len(gpus)
        chunk_size_gb = self.config.chunk_size / (1024 ** 3)

        for i, sender in enumerate(gpus):
            for j, receiver in enumerate(gpus):
                if i == j:
                    continue
                bandwidth = min(sender.config.bandwidth, receiver.config.bandwidth)
                duration = chunk_size_gb / bandwidth
                t = max(sender.clock, receiver.clock)
                sender.wait_until(t)
                receiver.wait_until(t)
                sender.execute_comm(duration)
                receiver.execute_comm(duration)
