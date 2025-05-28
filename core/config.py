from dataclasses import dataclass

@dataclass
class SystemConfig:
    num_gpus: int
    topology: str
    bandwidth: float  # GB/s
    compute_capability: float  # TFLOPS per GPU
    chunk_size: int  # bytes

    @staticmethod
    def from_dict(d):
        return SystemConfig(
            num_gpus=d["NUM_GPUS"],
            topology=d["TOPOLOGY"].upper(),
            bandwidth=d["NETWORK_BANDWIDTH"],
            compute_capability=d["COMPUTE_CAPABILITY"],
            chunk_size=d["COMMUNICATION_CHUNK_SIZE"]
        )
