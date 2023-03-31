from dataclasses import dataclass
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


@dataclass
class Session:
    # Identifier fields
    session_type: SessionType = None
    formula_type: FormulaType = None
    track: Track = None
    game_mode: GameMode = None
    session_length: SessionLength = None
    session_duration: int = None  # seconds
    weather: Weather = None

    # Other packet fields
    track_temp: int = None
    air_temp: int = None
    total_laps: int = None
    track_length: int = None
    session_time_left: int = None  # seconds
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
    rule_set: RuleSet = None
    time_of_day: int = None
    session_time_elapsed: int = 0

    # data not from packets
    participants: list = None
    final_classification: list = None

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.session_type != other.session_type:
            return False
        if self.track != other.track:
            return False
        if self.game_mode != other.game_mode:
            return False
        if self.session_length != other.session_length:
            return False
        return True
