import logging
from f1_22_telemetry.packets import (
    Packet,
    PacketCarDamageData,
    PacketCarTelemetryData,
    PacketCarStatusData,
    PacketCarSetupData,
    PacketLapData,
    PacketSessionData,
    PacketSessionHistoryData,
    PacketMotionData,
    PacketParticipantsData,
    PacketEventData,
    PacketFinalClassificationData,
    PacketLobbyInfoData
)
from managers.participant_manager import ParticipantManager

from managers.session_manager import SessionManager

_logger = logging.getLogger(__name__)


class Brain:
    def __init__(self):
        self.current_session = None
        self.previous_sessions = []

    def handle_received_packet(self, packet: Packet):
        packet_type = type(packet)
        _logger.debug(f'Handling new {packet_type}')

        if packet_type == PacketSessionData:
            self._handle_received_session_packet(packet)

        if packet_type == PacketParticipantsData:
            self._handle_received_participants_packet(packet)

    def _handle_received_session_packet(self, packet: PacketSessionData):
        tmp_session = SessionManager.create(packet)
        if not self.current_session:
            _logger.info('A new session has started')
            self.current_session = tmp_session
            return

        if self.current_session == tmp_session:
            changes = SessionManager.update(self.current_session, packet)
            if 'weather_forecast' in changes:
                print('Forecast has changed !')
                print(self.current_session.weather_forecast)
        else:
            _logger.info('A new session has started, previous one has been backuped')
            self.previous_sessions.append(self.current_session)
            self.current_session = tmp_session

    def _handle_received_participants_packet(self, packet:PacketParticipantsData):
        if not self.current_session:
            return # we could store in a tmp self. variable and store info at session creation if needed
        if not self.current_session.participants:
            self.current_session.participants = [
                ParticipantManager.create(packet.participants[i])
                for i in range(packet.num_active_cars)
            ]
        else:
            current_amount_of_participants = len(self.current_session.participants)
            for i in range(packet.num_active_cars):
                packet_data = packet.participants[i]
                if i > current_amount_of_participants - 1:
                    self.current_session.participants.append(ParticipantManager.create(packet_data))
                else:
                    changes = ParticipantManager.update(self.current_session.participants[i], packet_data)
                    if 'network_id' in changes or 'name' in changes:
                        _logger.warning('!? A participant changed !?')
                        _logger.warning(changes)
        
