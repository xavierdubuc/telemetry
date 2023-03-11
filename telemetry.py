from f1_22_telemetry.listener import TelemetryListener
from f1_22_telemetry.packets import *
import logging

from handlers.session_handler import SessionHandler
from command import Command

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

HANDLERS = {
    PacketCarDamageData: None,
    PacketCarTelemetryData: None,
    PacketCarStatusData: None,
    PacketCarSetupData: None,
    PacketLapData: None,
    PacketSessionData: SessionHandler(),
    PacketSessionHistoryData: None,
    PacketMotionData: None,
    PacketParticipantsData: None,#ParticipantsHandler(),
    PacketEventData: None,
    PacketFinalClassificationData: None,
}

_logger = logging.getLogger(__name__)
args = Command().parse_args()

_logger.info(f'Starting listening on {args.ip}:20777')
listener = TelemetryListener(host=args.ip)
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
