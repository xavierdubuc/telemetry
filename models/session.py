from datetime import timedelta
import logging
from dataclasses import dataclass
from f1_22_telemetry.packets import PacketSessionData
from models.session_type import SessionType
from models.weather import Weather
from models.track import Track
from models.formula_type import FormulaType
from models.gearbox import Gearbox
from models.racing_line_mode import RacingLineMode
from models.game_mode import GameMode
from models.rule_set import RuleSet
from models.session_length import SessionLength
from models.safety_car_status import SafetyCarStatus

_logger = logging.getLogger(__name__)


@dataclass
class Session:
    weather: Weather
    track_temp: int
    air_temp: int
    total_laps: int
    track_length: int
    session_type: SessionType
    track: Track
    formula_type: FormulaType
    session_time_left: int #seconds
    session_duration: int #seconds
    pit_speed_limit: int
    game_paused: bool
    is_spectating: bool
    spectator_car_index: int
    safety_car_status: SafetyCarStatus
    is_online: bool
    amount_of_pertinent_weather_forecast: int
    weather_forecast: list
    forecast_accuracy_is_perfect: bool
    ai_difficulty: int
    season_identifier: int
    weekend_identifier: int
    session_identifier: int
    pit_stop_window_start_lap: int
    pit_stop_window_end_lap: int
    pit_stop_rejoin_position: int
    gearbox: Gearbox
    help_steering_enabled: bool
    help_braking_enabled: bool
    help_pit: bool
    help_pit_release: bool
    help_ers: bool
    help_drs: bool
    racing_line_mode: RacingLineMode
    racing_line_is_3D: bool
    game_mode: GameMode
    rule_set: RuleSet
    time_of_day: int  # minutes since midnight FIXME better print
    session_length: SessionLength
    session_time_elapsed: int = 0

    def update(self, packet: PacketSessionData):
        self.session_time_left = packet.session_time_left
        self.session_duration = packet.session_duration
        self.session_time_elapsed = timedelta(seconds=self.session_duration - self.session_time_left)
        primitive_field_names = {
            'track_temp': 'track_temperature',
            'air_temp': 'air_temperature',
            'total_laps': 'total_laps',
            'track_length': 'track_length',
            'pit_speed_limit': 'pit_speed_limit',
            'spectator_car_index': 'spectator_car_index',
            'amount_of_pertinent_weather_forecast': 'num_weather_forecast_samples',
            'ai_difficulty': 'ai_difficulty',
            'season_identifier': 'season_link_identifier',
            'weekend_identifier': 'weekend_link_identifier',
            'session_identifier': 'session_link_identifier',
            'pit_stop_window_start_lap': 'pit_stop_window_ideal_lap',
            'pit_stop_window_end_lap': 'pit_stop_window_latest_lap',
            'pit_stop_rejoin_position': 'pit_stop_rejoin_position',
            'time_of_day': 'time_of_day',
        }
        for field, packet_field in primitive_field_names.items():
            packet_value = getattr(packet, packet_field)
            if getattr(self, field) != packet_value:
                setattr(self, field, packet_value)
                self._log(f'{field} changed, now is "{getattr(self, field)}"')

        enum_field_names = {
            'weather': (Weather, 'weather'),
            'session_type': (SessionType, 'session_type'),
            'track': (Track, 'track_id'),
            'formula_type': (FormulaType, 'formula'),
            'safety_car_status': (SafetyCarStatus, 'safety_car_status'),
            'gearbox': (Gearbox, 'gearbox_assist'),
            'racing_line_mode': (RacingLineMode, 'dynamic_racing_line'),
            'game_mode': (GameMode, 'game_mode'),
            'rule_set': (RuleSet, 'rule_set'),
            'session_length': (SessionLength, 'session_length'),
        }
        for field, (enum_class, packet_field) in enum_field_names.items():
            packet_value = getattr(packet, packet_field)
            if getattr(self, field).value != packet_value:
                setattr(self, field, enum_class(packet_value))
                self._log(f'{field} changed, now is "{getattr(self, field).name}"')

        bool_field_names = {
            'game_paused': 'game_paused',
            'is_spectating': 'is_spectating',
            'is_online': 'network_game',
            'help_steering_enabled': 'steering_assist',
            'help_braking_enabled': 'braking_assist',
            'help_pit': 'pit_assist',
            'help_pit_release': 'pit_release_assist',
            'help_ers': 'ers_assist',
            'help_drs': 'drs_assist',
            'racing_line_is_3D': 'dynamic_racing_line_type'
        }
        for field, packet_field in bool_field_names.items():
            packet_value = getattr(packet, packet_field) != 0
            if getattr(self, field) != packet_value:
                setattr(self, field, packet_value)
                self._log(f'''{field} changed, now is "{'enabled' if getattr(self, field) else 'disabled'}"''')

        if self.forecast_accuracy_is_perfect != (packet.forecast_accuracy == 0):
            packet_value = packet.forecast_accuracy == 0
            self.forecast_accuracy_is_perfect = packet_value
            self._log(f'''Forecast accuracy has changed, now is "{'Perfect' if packet_value else 'Approximate'}"''')

    def _log(self, txt):
        _logger.info(f'[{self.session_time_elapsed}] {txt}')