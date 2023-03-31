import logging
from dataclasses import dataclass, field
from typing import List
from models.evolving_model import EvolvingModel
from models.enums.result_status import ResultStatus
from models.enums.tyre import Tyre
from models.enums.tyre_compound import TyreCompound
from f1_22_telemetry.packets import PacketFinalClassificationData


@dataclass
class Classification:
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
