from enum import StrEnum

class BookingStatus(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELED"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]