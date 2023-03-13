import logging
from typing import List
from f1_22_telemetry.packets import PacketCarStatusData
from models.car_status import CarStatus
from handlers.abstract_handler import AbstractHandler

_logger = logging.getLogger(__name__)


class CarStatusHandler(AbstractHandler):

    def handle(self, packet: PacketCarStatusData):
        drivers = self.DB.get('drivers', [])
        if not drivers:
            self.DB.setdefault('drivers', [])
            for car_status_data in packet.car_status_data:
                _logger.info('New car status data created')
                drivers.append({'car_status': CarStatus.create(car_status_data)})
        else:
            for i, car_status_data in enumerate(packet.car_status_data):
                car_status = drivers[i].get('car_status')
                # an existing one is updated
                if not car_status:
                    drivers[i]['car_status'] = CarStatus.create(car_status_data)
                else:
                    drivers[i]['car_status'].update(car_status_data)
