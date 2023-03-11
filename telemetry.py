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
    _logger.info('Waiting for packets...')
    packet = listener.get()
    packet_type = type(packet)
    _logger.info(f'{packet_type} received...')
    handler = HANDLERS.get(packet_type)
    if handler:
        _logger.info('Handler found, handling the packet...')
        handler.handle(packet)
        _logger.info('Packet has been handled')
    else:
        _logger.info('No handler found for that packet, it has been ignored')
