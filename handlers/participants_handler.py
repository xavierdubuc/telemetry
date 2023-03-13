import logging
from typing import List
from f1_22_telemetry.packets import PacketParticipantsData
from models.participant import Participant
from handlers.abstract_handler import AbstractHandler

_logger = logging.getLogger(__name__)


KEY_DRIVERS = 'drivers'


class ParticipantsHandler(AbstractHandler):

    def handle(self, packet: PacketParticipantsData):
        drivers = self.DB.get('drivers', [])
        if not drivers:
            self.DB.setdefault('drivers', [])
            # no participant data yet
            for i in range(packet.num_active_cars):
                _logger.info('New participant data created')
                participant_data = packet.participants[i]
                print(f'{i}:{participant_data.name}')
                drivers.append({'participant': Participant.create(participant_data)})
        else:
            # already have participant data
            for i in range(packet.num_active_cars):
                participant_data = packet.participants[i]
                if i < len(drivers):
                    participant = drivers[i].get('participant')
                    # an existing one is updated
                    if not participant:
                        drivers[i]['participant'] = Participant.create(participant_data)
                    else:
                        drivers[i]['participant'].update(participant_data)
                else:
                    # a new participant joined ?
                    drivers.append({'participant': Participant.create(participant_data)})
