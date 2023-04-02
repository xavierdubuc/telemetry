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
from managers.classification_manager import ClassificationManager
from managers.damage_manager import DamageManager
from managers.lap_manager import LapManager
from managers.participant_manager import ParticipantManager

from managers.session_manager import SessionManager
from managers.telemetry_manager import TelemetryManager

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

        elif packet_type == PacketParticipantsData:
            self._handle_received_participants_packet(packet)

        elif packet_type == PacketFinalClassificationData:
            self._handle_received_final_classification_packet(packet)

        elif packet_type == PacketCarDamageData:
            self._handle_received_damage_packet(packet)

        elif packet_type == PacketCarTelemetryData:
            self._handle_received_telemetry_packet(packet)

        elif packet_type == PacketLapData:
            self._handle_received_lap_packet(packet)

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

    def _handle_received_damage_packet(self, packet:PacketCarDamageData):
        if not self.current_session:
            return # this should not happen
        if not self.current_session.participants:
            return # this should not happen neither
        amount_of_pertinent_damages = len(self.current_session.participants)
        if not self.current_session.damages:
            self.current_session.damages = [
                DamageManager.create(packet.car_damage_data[i])
                for i in range(amount_of_pertinent_damages)
            ]
        else:
            current_amount_of_damage = len(self.current_session.damages)
            for i in range(amount_of_pertinent_damages):
                packet_data = packet.car_damage_data[i]
                if i > current_amount_of_damage - 1:
                    self.current_session.damages.append(DamageManager.create(packet_data))
                else:
                    changes = DamageManager.update(self.current_session.damages[i], packet_data)
                    # if changes:
                    #     pilot = self.current_session.participants[i].name
                    #     _logger.warning(f'{pilot} had a change in damages !')
                    #     _logger.warning(changes)

    def _handle_received_telemetry_packet(self, packet:PacketCarTelemetryData):
        if not self.current_session:
            return # this should not happen
        if not self.current_session.participants:
            return # this should not happen neither
        amount_of_pertinent_telemetry = len(self.current_session.participants)
        if not self.current_session.telemetries:
            self.current_session.telemetries = [
                TelemetryManager.create(packet.car_telemetry_data[i])
                for i in range(amount_of_pertinent_telemetry)
            ]
        else:
            current_amount_of_telemetry = len(self.current_session.telemetries)
            for i in range(amount_of_pertinent_telemetry):
                packet_data = packet.car_telemetry_data[i]
                if i > current_amount_of_telemetry - 1:
                    self.current_session.telemetries.append(TelemetryManager.create(packet_data))
                else:
                    changes = TelemetryManager.update(self.current_session.telemetries[i], packet_data)
                    # if changes:
                        # pilot = self.current_session.participants[i].name
                        # _logger.info(f'{pilot} had a change in his telemetry !')
                        # _logger.info(changes)

    def _handle_received_final_classification_packet(self, packet:PacketFinalClassificationData):
        if not self.current_session:
            return # this should not happen
        if not self.current_session.final_classification:
            self.current_session.final_classification = [
                ClassificationManager.create(packet.classification_data[i])
                for i in range(packet.num_cars)
            ]
        else:
            current_amount_of_classification = len(self.current_session.final_classification)
            for i in range(packet.num_cars):
                packet_data = packet.classification_data[i]
                if i > current_amount_of_classification - 1:
                    self.current_session.final_classification.append(ClassificationManager.create(packet_data))
                else:
                    changes = ClassificationManager.update(self.current_session.final_classification[i], packet_data)
                    if changes:
                        _logger.warning('!? final classification changed !?')
                        _logger.warning(changes)

    def _handle_received_lap_packet(self, packet:PacketLapData):
        if not self.current_session:
            return # this should not happen
        if not self.current_session.participants:
            return # this should not happen neither
        amount_of_pertinent_lap = len(self.current_session.participants)
        if not self.current_session.laps:
            self.current_session.laps = [
                [LapManager.create(packet.lap_data[i], 0)]
                for i in range(amount_of_pertinent_lap)
            ]
        else:
            current_amount_of_lap = len(self.current_session.laps)
            for i in range(amount_of_pertinent_lap):
                packet_data = packet.lap_data[i]
                if i > current_amount_of_lap - 1:
                    self.current_session.laps.append([])

                car_laps = self.current_session.laps[i]
                car_last_lap = car_laps[-1] if car_laps else None
                if not car_last_lap or car_last_lap.current_lap_num != packet_data.current_lap_num:
                    car_laps.append(LapManager.create(packet_data, len(car_laps)))
                else:
                    changes = LapManager.update(car_last_lap, packet_data)

                    if 'car_position' in changes:
                        change = changes['car_position']
                        pilot = self.current_session.participants[i].name
                        delta = change.actual - change.old
                        if delta == 1:
                            _logger.warning(f'{pilot} gained a position ({change.old} -> {change.actual}) !')
                        elif delta > 1:
                            _logger.warning(f'{pilot} gained {delta} positions ({change.old} -> {change.actual}) !')
                        elif delta == -1:
                            _logger.warning(f'{pilot} lost a position ({change.old} -> {change.actual}) !')
                        elif delta < -1:
                            _logger.warning(f'{pilot} lost {delta} positions ({change.old} -> {change.actual}) !')

                #_logger.info(changes)