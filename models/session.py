from datetime import timedelta
import logging
from dataclasses import dataclass
from f1_22_telemetry.packets import PacketSessionData
from models.enums.session_type import SessionType
from models.enums.weather import Weather
from models.enums.track import Track
from models.enums.formula_type import FormulaType
from models.enums.gearbox import Gearbox
from models.enums.racing_line_mode import RacingLineMode
from models.enums.game_mode import GameMode
from models.enums.rule_set import RuleSet
from models.enums.session_length import SessionLength
from models.enums.safety_car_status import SafetyCarStatus
from models.evolving_model import EvolvingModel

_logger = logging.getLogger(__name__)


@dataclass
class Session(EvolvingModel):
    weather: Weather = None
    track_temp: int = None
    air_temp: int = None
    total_laps: int = None
    track_length: int = None
    session_type: SessionType = None
    track: Track = None
    formula_type: FormulaType = None
    session_time_left: int = None # seconds
    session_duration: int = None # seconds
    pit_speed_limit: int = None
    game_paused: bool = None
    is_spectating: bool = None
    spectator_car_index: int = None
    safety_car_status: SafetyCarStatus = None
    is_online: bool = None
    amount_of_pertinent_weather_forecast: int = None
    weather_forecast: list = None
    forecast_accuracy_is_perfect: bool = None
    ai_difficulty: int = None
    season_identifier: int = None
    weekend_identifier: int = None
    session_identifier: int = None
    pit_stop_window_start_lap: int = None
    pit_stop_window_end_lap: int = None
    pit_stop_rejoin_position: int = None
    gearbox: Gearbox = None
    help_steering_enabled: bool = None
    help_braking_enabled: bool = None
    help_pit: bool = None
    help_pit_release: bool = None
    help_ers: bool = None
    help_drs: bool = None
    racing_line_mode: RacingLineMode = None
    racing_line_is_3D: bool = None
    game_mode: GameMode = None
    rule_set: RuleSet = None
    time_of_day: int = None
    session_length: SessionLength = None
    session_time_elapsed: int = 0

    @staticmethod
    def _get_primitive_field_names():
        return {
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
        }

    @staticmethod
    def _get_enum_field_names():
        return {
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

    @staticmethod
    def _get_bool_field_names():
        return {
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

    def update(self, packet: PacketSessionData):
        self.session_time_left = packet.session_time_left
        self.session_duration = packet.session_duration
        self.session_time_elapsed = timedelta(seconds=self.session_duration - self.session_time_left)

        super(Session, self).update(packet)

        # time of day
        if self.time_of_day != packet.time_of_day:
            self.time_of_day = packet.time_of_day
            self._log(f'''Time of day is now {timedelta(minutes=self.time_of_day)}''')

        # forecast accuracy is perfect
        if self.forecast_accuracy_is_perfect != (packet.forecast_accuracy == 0):
            packet_value = packet.forecast_accuracy == 0
            self.forecast_accuracy_is_perfect = packet_value
            self._log(f'''Forecast accuracy has changed, now is "{'Perfect' if packet_value else 'Approximate'}"''')

    @classmethod
    def create(cls, packet: PacketSessionData):
        self = super().update(packet)

        self.session_time_left = packet.session_time_left
        self.session_duration = packet.session_duration
        self.session_time_elapsed = timedelta(seconds=self.session_duration - self.session_time_left)

        # time of day
        self.time_of_day = packet.time_of_day

        # forecast accuracy is perfect
        self.forecast_accuracy_is_perfect = packet.forecast_accuracy == 0

    def _log(self, txt):
        super(Session, self)._log(f'[{self.session_time_elapsed}] {txt}')
