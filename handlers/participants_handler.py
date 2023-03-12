import logging
from typing import List
from f1_22_telemetry.packets import PacketParticipantsData
from models.participant import Participant

_logger = logging.getLogger(__name__)


class ParticipantsHandler:
    participants_amount = 0
    participants:List[Participant] = []

    def handle(self, packet: PacketParticipantsData):
        if not self.participants:
            # no participant data yet
            for i in range(packet.num_active_cars):
                _logger.info('New participant data created')
                participant_data = packet.participants[i]
                # TODO can the index here be correlated with the index in LapData ?
                self.participants.append(Participant.create(participant_data))
        else:
            # already have participant data
            for i in range(packet.num_active_cars):
                _logger.info('New participant data created')
                participant_data = packet.participants[i]
                if i < len(self.participants):
                    # an existing one is updated
                    self.participants[i].update(participant_data)
                else:
                    # a new participant joined ?
                    self.participants.append(Participant.create(participant_data))

