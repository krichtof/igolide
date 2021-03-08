import struct
from adafruit_bluefruit_connect.packet import Packet

class EventPacket(Packet):
    SUCCESS = "1"
    WARNING = "2"
    START_POMODORO = "3"
    START_BREAK = "4"
    END_POMODORO = "5"
    DEFAULT_DURATION = 10

    _FMT_PARSE = "<xxsix"
    PACKET_LENGTH = struct.calcsize(_FMT_PARSE)
    _FMT_CONSTRUCT = "<2ssi"
    _TYPE_HEADER = b"!X"

    def __init__(self, event, duration=False):
        self._event = event
        self._duration = duration or self.DEFAULT_DURATION

    @classmethod
    def parse_private(cls, packet):
        event, duration = struct.unpack(cls._FMT_PARSE, packet)
        return cls(chr(event[0]), duration)

    def to_bytes(self):
        """Return the bytes needed to send this packet."""
        partial_packet = struct.pack(
                self._FMT_CONSTRUCT,
                self._TYPE_HEADER,
                self._event.encode("utf-8"),
                self._duration,
                )
        return self.add_checksum(partial_packet)

    @property
    def event(self):
        return self._event

    @property
    def duration(self):
        return self._duration


# Register this class with the superclass. This allows the user to import only what is needed.
EventPacket.register_packet_type()


