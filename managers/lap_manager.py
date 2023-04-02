from managers.abstract_manager import AbstractManager, Change
from models.enums.driver_status import DriverStatus
from models.enums.pit_status import PitStatus
from models.enums.result_status import ResultStatus
from models.lap import Lap
from f1_22_telemetry.packets import LapData


class LapManager(AbstractManager):
    model = Lap

    primitive_fields = {
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

    enum_fields = {
        'pit_status': (PitStatus, 'pit_status'),
        'driver_status': (DriverStatus, 'driver_status'),
        'result_status': (ResultStatus, 'result_status'),
    }

    bool_fields = {
        'current_lap_invalid': 'current_lap_invalid',
        'pit_lane_timer_active': 'pit_lane_timer_active',
    }

    @classmethod
    def create(cls, packet: LapData, index:int) -> Lap:
        self = super().create(packet)
        self.index = index
        return self