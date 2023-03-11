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

_logger = logging.getLogger(__name__)


@dataclass
class Session:
    weather: Weather = None
    track_temp: int
    air_temp: int
    total_laps: int
    track_length: int
    session_type: SessionType
    track: Track
    formula_type: FormulaType
    session_time_left: int
    session_duration: int
    pit_speed_limit: int
    game_paused: bool
    is_spectating: bool
    spectator_car_index: int
    # safety_car_status ?
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
    time_of_day: int  # minutes since midnight
    session_length: SessionLength

    def update(self, packet: PacketSessionData):
        if self.weather.value != packet.weather:
            self.weather = Weather(packet.weather)
            _logger.info(f'Weather changed, now is {self.weather.name}')
