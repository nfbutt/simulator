class Topology:
    def __init__(self, config):
        self.config = config

    def simulate_allreduce(self, gpus, size_gb):
        raise NotImplementedError


class RingTopology(Topology):
    def simulate_allreduce(self, gpus, size_gb):
        n = len(gpus)
        total_steps = 2 * (n - 1)
        chunk_size_gb = self.config.chunk_size / (1024 ** 3)
        print("chunk_size_gb = ", chunk_size_gb)
        num_chunks = int((size_gb / n) / chunk_size_gb)

        for step in range(total_steps):
            for i in range(n):
                sender = gpus[i]
                receiver = gpus[(i + 1) % n]
                duration = chunk_size_gb / self.config.bandwidth
                sender.wait_until(sender.clock)
                receiver.wait_until(sender.clock)
                sender.execute_comm(duration)
                receiver.execute_comm(duration)


class TreeTopology(Topology):
    def simulate_allreduce(self, gpus, size_gb):
        import math
        levels = int(math.ceil(math.log2(len(gpus))))
        chunk_size_gb = self.config.chunk_size / (1024 ** 3)
        duration = chunk_size_gb / self.config.bandwidth

        # Reduction
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

        # Broadcast
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
        n = len(gpus)
        chunk_size_gb = self.config.chunk_size / (1024 ** 3)
        duration = chunk_size_gb / self.config.bandwidth
        for sender in gpus:
            for receiver in gpus:
                if sender == receiver:
                    continue
                t = max(sender.clock, receiver.clock)
                sender.wait_until(t)
                receiver.wait_until(t)
                sender.execute_comm(duration)
                receiver.execute_comm(duration)
