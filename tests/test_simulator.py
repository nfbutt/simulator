import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

from core.config import SystemConfig
from core.simulator import Simulator
from core.events import Event


def test_simulation_runs():
    config = SystemConfig(
        num_gpus=4,
        topology="RING",
        bandwidth=25,
        compute_capability=200,
        chunk_size=512
    )
    sim = Simulator(config)
    events = [
        Event("COMPUTE", "ALL", "", 100, "EXECUTE"),
        Event("COMMUNICATION", "ALL", "", 16, "ALL_REDUCE"),
    ]
    sim.run(events)
    results = sim.results()
    assert len(results) == 4
    assert all(r["Clock"] > 0 for r in results)
    print("All tests passed.")


test_simulation_runs()