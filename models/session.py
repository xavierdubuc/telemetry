from dataclasses import dataclass
from datetime import timedelta

import pandas
from models.classification import Classification
from models.damage import Damage
from models.enums.result_status import ResultStatus
from models.enums.session_type import SessionType
from models.enums.tyre import Tyre
from models.enums.weather import Weather
from models.enums.track import Track
from models.enums.formula_type import FormulaType
from models.enums.gearbox import Gearbox
from models.enums.racing_line_mode import RacingLineMode
from models.enums.game_mode import GameMode
from models.enums.rule_set import RuleSet
from models.enums.session_length import SessionLength
from models.enums.safety_car_status import SafetyCarStatus
from typing import List
from models.lap import Lap

from models.participant import Participant
from models.telemetry import Telemetry


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
    participants: List[Participant] = None
    final_classification: List[Classification] = None
    damages: List[Damage] = None
    telemetries: List[Telemetry] = None
    laps: List[List[Lap]] = None

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

    def final_ranking_to_csv(self):
        data = []
        first_race_time = None
        for participant, classification in zip(self.participants, self.final_classification):
            current_tyres = ''.join([str(t) for t in classification.tyre_stints_visual])

            if classification.result_status in (ResultStatus.retired, ResultStatus.dnf, ResultStatus.not_classified):
                race_time = 'NT'
            elif classification.result_status == ResultStatus.dsq:
                race_time = 'DSQ'
            else:
                race_time = timedelta(seconds=classification.total_race_time)
            if classification.position == 1:
                first_race_time = race_time

            best_lap_time = self._format_time(timedelta(seconds=classification.best_lap_time_in_ms/1000))
            row = [
                classification.position, participant.name, race_time, current_tyres, best_lap_time
            ]
            data.append(row)

        for row in data:
            if row[0] != 1:
                if type(row[2]) != str:
                    row[2] = self._format_time(row[2] - first_race_time)
            else:
                row[2] = self._format_time(row[2])

        data.sort(key=lambda x: x[0])
        data = pandas.DataFrame(data)
        return data

    def _format_time(self, obj):
        minutes = obj.seconds//60
        minutes_str = f'{obj.seconds//60}:' if minutes > 0 else ''
        return f'{minutes_str}{obj.seconds%60}.{str(obj.microseconds//1000).zfill(3)}'