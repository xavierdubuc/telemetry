from datetime import timedelta
import logging
from dataclasses import dataclass
from f1_22_telemetry.packets import LapData
from models.evolving_model import EvolvingModel
from models.enums.driver_status import DriverStatus
from models.enums.pit_status import PitStatus
from models.enums.result_status import ResultStatus

_logger = logging.getLogger(__name__)


@dataclass
class Lap(EvolvingModel):
    last_lap_time_in_ms: int = None
    current_lap_time_in_ms: int = None
    sector1_time_in_ms: int = None
    sector2_time_in_ms: int = None
    lap_distance: float = None
    total_distance: float = None
    safety_car_delta: float = None
    car_position: int = None
    current_lap_num: int = None
    pit_status: PitStatus = None
    num_pit_stops: int = None
    sector: int = None
    current_lap_invalid: bool = None
    penalties: int = None
    warnings: int = None
    num_unserved_drive_through_pens: int = None
    num_unserved_stop_go_pens: int = None
    grid_position: int = None
    driver_status: DriverStatus = None
    result_status: ResultStatus = None
    pit_lane_timer_active: bool = None
    pit_stop_timer_in_ms: int = None
    pit_lane_time_in_lane_in_ms: int = None
    pit_stop_should_serve_pen: int = None

    def _get_primitive_field_names(self):
        return {
            'last_lap_time_in_ms': 'last_lap_time_in_ms',
            'current_lap_time_in_ms': 'current_lap_time_in_ms',
            'sector1_time_in_ms': 'sector1_time_in_ms',
            'sector2_time_in_ms': 'sector2_time_in_ms',
            'lap_distance': 'lap_distance',
            'total_distance': 'total_distance',
            'safety_car_delta': 'safety_car_delta',
            'car_position': 'car_position',
            'current_lap_num': 'current_lap_num',
            'num_pit_stops': 'num_pit_stops',
            'sector': 'sector',
            'penalties': 'penalties',
            'warnings': 'warnings',
            'num_unserved_drive_through_pens': 'num_unserved_drive_through_pens',
            'num_unserved_stop_go_pens': 'num_unserved_stop_go_pens',
            'grid_position': 'grid_position',
            'pit_stop_timer_in_ms': 'pit_stop_timer_in_ms',
            'pit_lane_time_in_lane_in_ms': 'pit_lane_time_in_lane_in_ms',
            'pit_stop_should_serve_pen': 'pit_stop_should_serve_pen',
        }

    def _get_enum_field_names(self):
        return {
            'pit_status': 'pit_status',
            'driver_status': 'driver_status',
            'result_status': 'result_status',
        }

    def _get_bool_field_names(self):
        return {
            'current_lap_invalid': 'current_lap_invalid',
            'pit_lane_timer_active': 'pit_lane_timer_active',
        }