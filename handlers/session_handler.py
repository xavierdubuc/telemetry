import logging
from f1_22_telemetry.packets import PacketSessionData
from models.session import Session
from models.enums.weather import Weather
from models.enums.session_type import SessionType
from models.enums.track import Track
from models.enums.formula_type import FormulaType
from models.enums.gearbox import Gearbox
from models.enums.racing_line_mode import RacingLineMode
from models.enums.game_mode import GameMode
from models.enums.rule_set import RuleSet
from models.enums.session_length import SessionLength
from models.enums.safety_car_status import SafetyCarStatus

_logger = logging.getLogger(__name__)


class SessionHandler:
    session = None

    def handle(self, packet: PacketSessionData):
        if not self.session:
            self.session = Session(
                weather=Weather(packet.weather),
                track_temp=packet.track_temperature,
                air_temp=packet.air_temperature,
                total_laps=packet.total_laps,
                track_length=packet.track_length,
                session_type=SessionType(packet.session_type),
                track=Track(packet.track_id),
                formula_type=FormulaType(packet.formula),
                session_time_left=packet.session_time_left,
                session_duration=packet.session_duration,
                pit_speed_limit=packet.pit_speed_limit,
                game_paused=packet.game_paused != 0,
                is_spectating=packet.is_spectating != 0,
                spectator_car_index=packet.spectator_car_index,
                safety_car_status=SafetyCarStatus(packet.safety_car_status),
                is_online=packet.network_game != 0,
                amount_of_pertinent_weather_forecast=packet.num_weather_forecast_samples,
                weather_forecast=packet.weather_forecast_samples,
                forecast_accuracy_is_perfect=packet.forecast_accuracy == 0,
                ai_difficulty=packet.ai_difficulty,
                season_identifier=packet.season_link_identifier,
                weekend_identifier=packet.weekend_link_identifier,
                session_identifier=packet.session_link_identifier,
                pit_stop_window_start_lap=packet.pit_stop_window_ideal_lap,
                pit_stop_window_end_lap=packet.pit_stop_window_latest_lap,
                help_steering_enabled=packet.steering_assist != 0,
                help_braking_enabled=packet.braking_assist != 0,
                gearbox=Gearbox(packet.gearbox_assist),
                help_pit=packet.pit_assist,
                help_pit_release=packet.pit_release_assist,
                help_ers=packet.ers_assist,
                help_drs=packet.drs_assist,
                racing_line_mode=RacingLineMode(packet.dynamic_racing_line),
                racing_line_is_3D=packet.dynamic_racing_line_type != 0,
                game_mode=GameMode(packet.game_mode),
                rule_set=RuleSet(packet.rule_set),
                time_of_day=packet.time_of_day,
                session_length=SessionLength(packet.session_length)
            )
        else:
            self.session.update(packet)
