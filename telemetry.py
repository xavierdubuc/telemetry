import sys
from f1_22_telemetry.listener import TelemetryListener
from f1_22_telemetry.packets import *
import logging

from handlers.participants_handler import ParticipantsHandler
from handlers.lap_handler import LapHandler
from handlers.session_handler import SessionHandler
from handlers.car_status_handler import CarStatusHandler
from command import Command
from telemetry.handlers.lobby_handler import LobbyHandler

DB = {
    'session': None,
    'drivers': [
        # with elements like 
        # {
        #   'participant' : Participant
        #   'lobby_driver' : LobbyDriver
        #   'laps': [] of Lap,
        #   'car_status': CarStatus
        # }
    ]
}
HANDLERS = {
    PacketCarDamageData: None,
    PacketCarTelemetryData: None,
    PacketCarStatusData: CarStatusHandler(DB),
    PacketCarSetupData: None,
    PacketLapData: LapHandler(DB),
    PacketSessionData: SessionHandler(DB),
    PacketSessionHistoryData: None,
    PacketMotionData: None,
    PacketParticipantsData: ParticipantsHandler(DB),
    PacketEventData: None,
    PacketFinalClassificationData: None,
    PacketLobbyInfoData: LobbyHandler(DB),
}

args = Command().parse_args()
levels = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}
log_level = levels[args.log_level]
print(f'Using log level : "{args.log_level}"')
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
_logger = logging.getLogger(__name__)

_logger.info(f'Starting listening on {args.ip}:20777')
listener = TelemetryListener(host=args.ip)
try:
    while True:
        _logger.debug('Waiting for packets...')
        packet = listener.get()
        packet_type = type(packet)
        _logger.debug(f'{packet_type} received...')
        handler = HANDLERS.get(packet_type)
        if handler:
            _logger.debug(f'Handling new {packet_type}')
            handler.handle(packet)
            _logger.debug(str(packet))
            _logger.debug('Packet has been handled')
        else:
            _logger.debug('No handler found for that packet, it has been ignored')
except KeyboardInterrupt:
    _logger.info('Stopping telemetry...')
    with open("session.json", "w") as out_file:
        json.dump(DB, out_file)
    sys.exit(130)
except:
    _logger.info('Stopping telemetry because of huge fail...')
    with open("session.json", "w") as out_file:
        json.dump(DB, out_file)
    sys.exit(1)
