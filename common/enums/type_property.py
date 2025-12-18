from enum import StrEnum

class PropertyType(StrEnum):
    FLAT = "FLAT"
    HOUSE = "HOUSE"
    STUDIO = "STUDIO"
    ROOM = "ROOM"

    @classmethod
    def choices(cls):
        return [(attr.value, attr.value) for attr in cls]