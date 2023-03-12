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
            self.session = Session.create(packet)
        else:
            self.session.update(packet)
