import logging
from dataclasses import dataclass, field
from typing import List
from models.evolving_model import EvolvingModel
from models.enums.result_status import ResultStatus
from models.enums.tyre import Tyre
from models.enums.tyre_compound import TyreCompound
from f1_22_telemetry.packets import PacketFinalClassificationData


@dataclass
class Classification(EvolvingModel):
    position: int = None
    grid_position: int = None
    num_laps: int = None
    points: int = None
    num_pit_stops: int = None
    total_race_time: float = None #in seconds, without penalties
    penalties_time: int = None # total amount of time
    num_penalties: int = None # total amount
    num_tyre_stints: int = None
    best_lap_time_in_ms: int = None
    result_status: ResultStatus = None
    tyre_stints_actual: List[TyreCompound] = field(default_factory=list)
    tyre_stints_visual: List[Tyre] = field(default_factory=list)
    tyre_stints_end_laps: List[int] = field(default_factory=list)

    @classmethod
    def create(cls, packet: PacketFinalClassificationData):
        self = super().create(packet)
        self.tyre_stints_actual = [TyreCompound(tyre) for tyre in packet.tyre_stints_actual]
        self.tyre_stints_visual = [Tyre(tyre) for tyre in packet.tyre_stints_visual]
        self.tyre_stints_end_laps = packet.tyre_stints_end_laps

    @staticmethod
    def _get_primitive_field_names():
        return {
            'position': 'position',
            'grid_position': 'grid_position',
            'num_laps': 'num_laps',
            'points': 'points',
            'num_pit_stops': 'num_pit_stops',
            'total_race_time': 'total_race_time',
            'penalties_time': 'penalties_time',
            'num_penalties': 'num_penalties',
            'num_tyre_stints': 'num_tyre_stints',
            'best_lap_time_in_ms': 'best_lap_time_in_ms',
        }

    @staticmethod
    def _get_enum_field_names():
        return {
            'result_status': (ResultStatus, 'result_status'),
        }

    @staticmethod
    def _get_bool_field_names():
        return {}