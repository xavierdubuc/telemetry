import unittest
from unittest.mock import Mock, call, patch
from f1_22_telemetry.packets import (
    PacketSessionData,
    PacketParticipantsData,
    ParticipantData
)

from brain import Brain
from models.enums.nationality import Nationality
from models.enums.team import Team
from models.enums.track import Track
from models.participant import Participant
from models.session import Session

class BrainTest(unittest.TestCase):
    def setUp(self):
        self.brain = Brain()

    @patch('brain.Brain._handle_received_participants_packet')
    @patch('brain.Brain._handle_received_session_packet')
    def test_handle_received_packet(self, patch_session, patch_participant):
        packet = PacketSessionData()
        self.brain.handle_received_packet(packet)
        patch_session.assert_called_once_with(packet)
        patch_participant.assert_not_called()

        patch_session.reset_mock()
        packet = PacketParticipantsData()
        self.brain.handle_received_packet(packet)
        patch_participant.assert_called_once_with(packet)
        patch_session.assert_not_called()

    @patch('managers.session_manager.SessionManager.update')
    @patch('managers.session_manager.SessionManager.create')
    def test__handle_received_session_packet(self, patched_create, patched_update):
        # no current session
        session = Session(track=Track.spa)
        patched_create.return_value = session
        packet = PacketSessionData(track_id=10)

        self.brain._handle_received_session_packet(packet)
        patched_create.assert_called_once_with(packet)
        self.assertEqual(self.brain.current_session, session)
        self.assertListEqual(self.brain.previous_sessions, [])
        patched_update.assert_not_called()

        # session didn't change
        patched_create.reset_mock()
        new_session = Session(track=Track.spa)
        patched_create.return_value = new_session

        self.brain._handle_received_session_packet(packet)
        patched_create.assert_called_once_with(packet)
        self.assertEqual(self.brain.current_session, session)
        self.assertListEqual(self.brain.previous_sessions, [])
        patched_update.assert_called_once_with(session, packet)

        # session changed
        patched_create.reset_mock()
        patched_update.reset_mock()
        new_session = Session(track=Track.hungaroring)
        packet = PacketSessionData(track_id=Track.hungaroring.value)
        patched_create.return_value = new_session

        self.brain._handle_received_session_packet(packet)
        patched_create.assert_called_once_with(packet)
        self.assertEqual(self.brain.current_session, new_session)
        self.assertListEqual(self.brain.previous_sessions, [session])
        patched_update.assert_not_called()

    @patch('managers.participant_manager.ParticipantManager.update')
    @patch('managers.participant_manager.ParticipantManager.create')
    def test__handle_received_participants_packet(self, patched_create, patched_update):
        xion = Participant(name="Xion")
        prolactron = Participant(name="Prolactron")
        cid = Participant(name="Cid")
        participants_data = [
            ParticipantData(
                ai_controlled=False, driver_id=255, network_id=1,
                team_id=Team.alfa_romeo.value, my_team=0, race_number=2,
                nationality=Nationality.belgian.value, name=b'Xionhearts', your_telemetry=1
            ),
            ParticipantData(
                ai_controlled=False, driver_id=255, network_id=2,
                team_id=Team.ferrari.value, my_team=0, race_number=26,
                nationality=Nationality.turkish.value, name=b'Prolactron', your_telemetry=1
            ),
        ]
        packet = PacketParticipantsData(num_active_cars=2, participants=(ParticipantData * 22)(*participants_data))

        self.brain._handle_received_participants_packet(packet)
        patched_create.assert_not_called()
        patched_update.assert_not_called()
        patched_create.side_effect = [xion, prolactron, cid]

        self.brain.current_session = Session()

        self.brain._handle_received_participants_packet(packet)
        self.assertEqual(patched_create.call_count, 2)
        self.assertEqual(str(patched_create.call_args_list[0][0][0]), str(packet.participants[0]))
        self.assertEqual(str(patched_create.call_args_list[1][0][0]), str(packet.participants[1]))
        patched_update.assert_not_called()
        self.assertListEqual(self.brain.current_session.participants, [xion, prolactron])

        patched_create.reset_mock()
        patched_update.reset_mock()
        participants_data[1].team_id = Team.aston_martin.value
        participants_data.append(
            ParticipantData(
                ai_controlled=False, driver_id=255, network_id=3,
                team_id=Team.mercedes.value, my_team=0, race_number=16,
                nationality=Nationality.belgian.value, name=b'FBRT_CiD16', your_telemetry=1
            )
        )
        new_packet = PacketParticipantsData(num_active_cars=3, participants=(ParticipantData * 22)(*participants_data))

        self.brain._handle_received_participants_packet(new_packet)
        self.assertEqual(patched_update.call_count , 2)
        self.assertEqual(patched_update.call_args_list[0][0][0], xion)
        self.assertEqual(patched_update.call_args_list[1][0][0], prolactron)
        self.assertEqual(str(patched_update.call_args_list[0][0][1]), str(new_packet.participants[0]))
        self.assertEqual(str(patched_update.call_args_list[1][0][1]), str(new_packet.participants[1]))
        patched_create.assert_called_once()
        self.assertEqual(str(patched_create.call_args[0][0]), str(new_packet.participants[2]))
