from enum import StrEnum

class Roles(StrEnum):
    RENTER = "renter"
    LANDLORD = "landlord"

    @classmethod
    def choices(cls):
        return [(attr.value, attr.value) for attr in cls]
