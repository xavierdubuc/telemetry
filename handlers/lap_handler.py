import logging
from typing import List
from f1_22_telemetry.packets import PacketLapData
from models.enums.driver_status import DriverStatus
from models.enums.pit_status import PitStatus
from models.enums.result_status import ResultStatus
from models.lap import Lap

_logger = logging.getLogger(__name__)


class LapHandler:
    lap_info_by_cars:List[List[Lap]] = []

    def handle(self, packet: PacketLapData):
        if not self.lap_info_by_cars:
            # no lap data yet
            for i, lap_data in enumerate(packet.lap_data):
                _logger.info('New driver lap data created')
                self.lap_info_by_cars.append([Lap.create(lap_data, index=i)])
        else:
            # already have lap data
            for i, lap_data in enumerate(packet.lap_data):
                car_laps = self.lap_info_by_cars[i]
                car_last_lap = car_laps[-1]
                # driver is still in same lap --> update data
                if car_last_lap.current_lap_num == lap_data.current_lap_num:
                    car_last_lap.update(lap_data)
                else:
                    # driver finished a lap --> dump old lap and create new one
                    _logger.info(f'Driver #{i} starts a new lap')
                    with open('./data/laps/{i}.log', 'w+') as lap_file:
                        lap_file.writelines([
                            f'---- Lap # {len(car_laps)}',
                            str(car_last_lap),
                            "\n"
                        ])
                    car_laps.append(Lap.create(lap_data, index=i))

