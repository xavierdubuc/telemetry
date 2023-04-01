from dataclasses import dataclass


@dataclass
class Damage:
    tyres_wear: float
    tyres_damage: int
    brakes_damage: int
    front_left_wing_damage: int
    front_right_wing_damage: int
    rear_wing_damage: int
    floor_damage: int
    diffuser_damage: int
    sidepod_damage: int
    drs_fault: bool
    ers_fault: bool
    gearbox_damage: int
    engined_damage: int
    engine_mguh_wear: int
    engine_energy_store_qear: int
    engine_control_electronics_wear: int
    engine_internal_combustion_engine_wear: int
    engine_mguk_wear: int
    engine_traction_control_wear: int
    engine_blown: bool
    engine_seized: bool
