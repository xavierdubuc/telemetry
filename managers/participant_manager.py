from discord import Team
from models.enums.nationality import Nationality
from models.enums.original_driver import OriginalDriver
from models.participant import Participant
from managers.abstract_manager import AbstractManager


class ParticipantManager(AbstractManager):
    model = Participant

    primitive_fields = {
        'network_id': 'network_id',
        'race_number': 'race_number',
        'name': 'name',
    }

    enum_fields = {
        'original_driver': (OriginalDriver, 'driver_id'),
        'team': (Team, 'team_id'),
        'nationality': (Nationality, 'nationality'),
    }

    bool_fields = {
        'is_my_team_mode': 'my_team',
        'ai_controlled': 'ai_controlled',
        'telemetry_is_public': 'your_telemetry',
    }
