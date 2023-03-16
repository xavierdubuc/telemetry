import logging
from f1_22_telemetry.packets import PacketFinalClassificationData
from models.classification import Classification
from handlers.abstract_handler import AbstractHandler

_logger = logging.getLogger(__name__)


KEY_DRIVERS = 'drivers'


class FinalClassificationHandler(AbstractHandler):

    def handle(self, packet: PacketFinalClassificationData):
        drivers = self.DB.get('drivers', [])
        if not drivers:
            self.DB.setdefault('drivers', [])
            # no classification data yet
            for i in range(packet.num_cars):
                _logger.info('New classification data created')
                classification_data = packet.classification_data[i]
                drivers.append({'final_classification': Classification.create(classification_data)})
        else:
            # already have classification data
            for i in range(packet.num_cars):
                classification_data = packet.classification_data[i]
                if i < len(drivers):
                    classification = drivers[i].get('final_classification')
                    # an existing one is updated
                    if not classification:
                        drivers[i]['final_classification'] = Classification.create(classification_data)
                    else:
                        drivers[i]['final_classification'].update(classification_data)
                else:
                    # a new classification joined ?
                    drivers.append({'final_classification': Classification.create(classification_data)})
