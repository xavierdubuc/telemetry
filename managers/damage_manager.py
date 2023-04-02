from typing import Dict
from managers.abstract_manager import AbstractManager, Change
from models.damage import Damage
from f1_22_telemetry.packets import CarDamageData


class DamageManager(AbstractManager):
    model = Damage

    primitive_fields = {
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

    @classmethod
    def create(cls, packet: CarDamageData) -> Damage:
        self = super().create(packet)
        self.tyres_wear = list(packet.tyres_wear)
        return self

    @classmethod
    def update(cls, damage: Damage, packet: CarDamageData) -> Dict[str, Change]:
        changes = super().update(damage, packet)
        new_value = list(packet.tyres_wear)
        old_value = damage.tyres_wear
        if new_value != old_value:
            changes['tyres_wear']= Change(actual=new_value, old=old_value)
            damage.tyres_wear = new_value

        return changes
