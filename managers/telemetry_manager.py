from managers.abstract_manager import AbstractManager, Change
from models.telemetry import Telemetry
from f1_22_telemetry.packets import CarTelemetryData


class TelemetryManager(AbstractManager):
    model = Telemetry

    primitive_fields = {
        'speed': 'speed',
        'throttle': 'throttle',
        'steer': 'steer',
        'brake': 'brake',
        'gear': 'gear',
        'engine_rpm': 'engine_rpm',
        'rev_lights_percent': 'rev_lights_percent',
        'rev_lights_bit_value': 'rev_lights_bit_value',
        'engine_temperature': 'engine_temperature',
        # brakes_temperature
        # tyres_surface_temperature
        # tyres_inner_temperature
        # tyres_pressure
        # surface_type
    }

    enum_fields = {}

    bool_fields = {
        'drs': 'drs',
    }

    @classmethod
    def create(cls, packet: CarTelemetryData) -> Telemetry:
        self = super().create(packet)
        self.brakes_temperature = list(packet.brakes_temperature)
        self.tyres_surface_temperature = list(packet.tyres_surface_temperature)
        self.tyres_inner_temperature = list(packet.tyres_inner_temperature)
        self.tyres_pressure = list(packet.tyres_pressure)
        self.surface_type = list(packet.surface_type)
        return self

    @classmethod
    def update(cls, telemetry:Telemetry, packet: CarTelemetryData) -> dict:
        changes = super().update(telemetry, packet)

        list_fields = [
            'brakes_temperature','tyres_surface_temperature',
            'tyres_inner_temperature','tyres_pressure','surface_type',
        ]
        for field in list_fields:
            new_value = list(getattr(packet, field))
            old_value = getattr(telemetry, field)
            if new_value != old_value:
                changes[field]= Change(actual=new_value, old=old_value)
                setattr(telemetry, field, new_value)

        return changes
