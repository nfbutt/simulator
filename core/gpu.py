class GPU:
    def __init__(self, gpu_id, config):
        self.gpu_id = gpu_id
        self.clock = 0.0
        self.config = config
        self.events = []
        self.computation_time = 0.0
        self.communication_time = 0.0

    def execute_compute(self, flops):
        time = flops / (self.config.compute_capability * 1e12)  # in seconds
        self.clock += time
        self.computation_time += time

    def wait_until(self, time):
        self.clock = max(self.clock, time)

    def execute_comm(self, duration):
        self.clock += duration
        self.communication_time += duration
