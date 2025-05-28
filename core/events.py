class Event:
    def __init__(self, event_type, source, dest, size, op):
        self.event_type = event_type
        self.source = source
        self.dest = dest
        self.size = size
        self.op = op

    @staticmethod
    def from_line(line):
        parts = [p.strip() for p in line.split(',')]
        return Event(
            event_type=parts[0],
            source=parts[1],
            dest=parts[2],
            size=int(parts[3]),
            op=parts[4]
        )



