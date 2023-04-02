import sys
import pickle
from datetime import datetime
from disnake.ext import commands
from f1_22_telemetry.listener import TelemetryListener
from f1_22_telemetry.packets import *
import logging
from brain import Brain


_logger = logging.getLogger(__name__)


def run_telemetry(ip:str, bot:commands.InteractionBot):
    brain = Brain()
    _logger.info(f'Starting listening on {ip}:20777')
    listener = TelemetryListener(host=ip)
    i = 0
    try:
        while True:
            _logger.debug('Waiting for packets...')
            packet = listener.get()
            packet_type = type(packet)
            _logger.debug(f'{packet_type} received...')
            brain.handle_received_packet(packet)
            if brain.current_session and brain.current_session.participants:
                for participant in brain.current_session.participants:
                    if not participant.telemetry_is_public:
                        print(f'{participant.race_number} {participant.name} does not have public telemetry !')
            i += 1
    except KeyboardInterrupt:
        _logger.info('Stopping telemetry...')
        with open(f"session{datetime.now().isoformat()}.pickle", "wb") as out_file:
            pickle.dump(brain, out_file)
        sys.exit(130)
    except:
        _logger.info('Stopping telemetry because of huge fail...')
        with open(f"session{datetime.now().isoformat()}.pickle", "wb") as out_file:
            pickle.dump(brain, out_file)
        raise