from core.events import Event

def parse_trace_file(path):
    with open(path) as f:
        lines = f.readlines()
    return [
        Event.from_line(line)
        for line in lines
        if not line.startswith("#") and line.strip()
    ]
