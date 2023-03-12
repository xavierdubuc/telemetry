import logging
from dataclasses import dataclass
from models.evolving_model import EvolvingModel
from models.enums.team import Team
from models.enums.original_driver import OriginalDriver
from models.enums.nationality import Nationality

_logger = logging.getLogger(__name__)


@dataclass
class Participant(EvolvingModel):
    network_id: int = None
    race_number: int = None
    name: int = None
    original_driver: OriginalDriver = None
    team: Team = None
    nationality: Nationality = None
    is_my_team_mode: bool = None
    ai_controlled: bool = None
    telemetry_is_public: bool = None

    def __str__(self):
        return f'"{self.name}" (#{self.race_number}), {self.nationality.name}, driving the {self.team.name} car of {self.original_driver.name}'

    @staticmethod
    def _get_primitive_field_names():
        return {
            'network_id': 'network_id',
            'race_number': 'race_number',
            'name': 'name',
        }

    @staticmethod
    def _get_enum_field_names():
        return {
            'original_driver': (OriginalDriver, 'driver_id'),
            'team': (Team,'team_id'),
            'nationality': (Nationality,'nationality'),
        }

    @staticmethod
    def _get_bool_field_names():
        return {
            'is_my_team_mode': 'my_team',
            'ai_controlled': 'ai_controlled',
            'telemetry_is_public': 'your_telemetry',
        }