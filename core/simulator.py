from core.gpu import GPU
from core.topology import RingTopology, TreeTopology, FullyConnectedTopology

class Simulator:
    def __init__(self, config):
        self.config = config
        self.gpus = [GPU(i, config) for i in range(config.num_gpus)]
        self.topology = self._init_topology()

    def _init_topology(self):
        t = self.config.topology
        if t == 'RING':
            return RingTopology(self.config)
        elif t == 'TREE':
            return TreeTopology(self.config)
        elif t == 'FULLY_CONNECTED':
            return FullyConnectedTopology(self.config)
        raise ValueError(f"Unsupported topology: {t}")

    def run(self, events):
        for event in events:
            if event.event_type == "COMPUTE":
                flops = event.size * 1e12
                for gpu in self.gpus:
                    gpu.execute_compute(flops)
            elif event.event_type == "COMMUNICATION" and event.op == "ALL_REDUCE":
                size_gb = event.size
                self.topology.simulate_allreduce(self.gpus, size_gb)

    def results(self):
        return [
            {
                "GPU": g.gpu_id,
                "Clock": g.clock,
                "Compute Time": g.computation_time,
                "Comm Time": g.communication_time
            }
            for g in self.gpus
        ]
