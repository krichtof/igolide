import json
from event_packet import EventPacket

class Event:
    @classmethod
    def from_request(cls, request):
        print(request.headers)
        print(request.form['payload'])
        if "X-Github-Event" in request.headers.keys():
            payload = json.loads(request.form['payload'])
            return GithubEvent(payload)
        return None

class GithubEvent(Event):
    @classmethod
    def __init__(self, payload):
        if payload["ref"] == "refs/heads/dev":
            self._packet = EventPacket(EventPacket.SUCCESS, 10)
        else:
            self._packet = None


    @property
    def packet(self):
        return self._packet
