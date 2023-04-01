from managers.abstract_manager import AbstractManager
from models.damage import Damage


class DamageManager(AbstractManager):
    model = Damage

    primitive_fields = {
        'tyres_wear': 'tyres_wear',
        'tyres_damage': 'tyres_damage',
        'brakes_damage': 'brakes_damage',
        'front_left_wing_damage': 'front_left_wing_damage',
        'front_right_wing_damage': 'front_right_wing_damage',
        'rear_wing_damage': 'rear_wing_damage',
        'floor_damage': 'floor_damage',
        'diffuser_damage': 'diffuser_damage',
        'sidepod_damage': 'sidepod_damage',
        'gearbox_damage': 'gearbox_damage',
        'engined_damage': 'engined_damage',
        'engine_mguh_wear': 'engine_mguh_wear',
        'engine_energy_store_qear': 'engine_energy_store_qear',
        'engine_control_electronics_wear': 'engine_control_electronics_wear',
        'engine_internal_combustion_engine_wear': 'engine_internal_combustion_engine_wear',
        'engine_mguk_wear': 'engine_mguk_wear',
        'engine_traction_control_wear': 'engine_traction_control_wear',
    }

    enum_fields = {}

    bool_fields = {
        'drs_fault': 'drs_fault',
        'ers_fault': 'ers_fault',
        'engine_blown': 'engine_blown',
        'engine_seized': 'engine_seized',
    }
