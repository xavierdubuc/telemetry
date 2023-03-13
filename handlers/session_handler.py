from f1_22_telemetry.packets import PacketSessionData
from models.session import Session
from handlers.abstract_handler import AbstractHandler


class SessionHandler(AbstractHandler):
    session = None

    def handle(self, packet: PacketSessionData):
        if not self.DB.get('session'):
            self.DB['session'] = Session.create(packet)
        else:
            self.DB['session'].update(packet)
