import logging
from typing import List
from f1_22_telemetry.packets import PacketLobbyInfoData
from models.lobby_player import LobbyPlayer
from handlers.abstract_handler import AbstractHandler

_logger = logging.getLogger(__name__)


class LobbyHandler(AbstractHandler):
    def handle(self, packet: PacketLobbyInfoData):
        drivers = self.DB.get('drivers', [])
        if not drivers:
            self.DB.setdefault('drivers', [])
            # no lobby player data yet
            for i in range(packet.num_players):
                _logger.info('New lobby player data created')
                lobby_player_data = packet.lobby_players[i]
                print(f'{i}:{lobby_player_data.name}')
                drivers.append({'lobby_driver': LobbyPlayer.create(lobby_player_data)})
        else:
            # already have player data
            for i in range(packet.num_players):
                lobby_player_data = packet.lobby_players[i]
                if i < len(drivers):
                    participant = drivers[i].get('lobby_driver')
                    # an existing one is updated
                    if not participant:
                        drivers[i]['lobby_driver'] = LobbyPlayer.create(lobby_player_data)
                    else:
                        drivers[i]['lobby_driver'].update(lobby_player_data)
                else:
                    # a new player joined ?
                    drivers.append({'lobby_driver': LobbyPlayer.create(lobby_player_data)})

