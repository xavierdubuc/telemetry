import logging
from typing import List
from f1_22_telemetry.packets import PacketCarStatusData
from models.car_status import CarStatus

_logger = logging.getLogger(__name__)


class CarStatusHandler:
    car_statuses: List[CarStatus] = []

    def handle(self, packet: PacketCarStatusData):
        if not self.car_statuses:
            # no participant data yet
            for car_status_data in packet.car_status_data:
                _logger.info('New car status data created')
                # TODO car status index =? lap index --> si oui, voir pour merger les objets ou les lier
                self.car_statuses.append(CarStatus.create(car_status_data))
        else:
            # already have participant data
            for i, car_status_data in enumerate(packet.car_status_data):
                self.car_statuses[i].update(car_status_data)
