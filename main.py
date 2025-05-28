import sys
import json
from core.simulator import Simulator
from core.config import SystemConfig
from utils.parser import parse_trace_file


if __name__ == "__main__":
    if not sys.argv[1].endswith('.json') or not sys.argv[2].endswith('.csv'):
        print("Usage: python main.py <config.json> <trace.csv>")
        print("Error: First argument must be a JSON file and second argument must be a CSV file.")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        config_dict = json.load(f)

        events = parse_trace_file(sys.argv[2])
        # print(events)

        config = SystemConfig.from_dict(config_dict)

        sim = Simulator(config)
        sim.run(events)
        for r in sim.results():
            print(r)




