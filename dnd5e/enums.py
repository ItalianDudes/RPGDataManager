from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.enums import StrEnum


#   COMMON = ("Comune", "#E0E0E0FF")
#   UNCOMMON = ("Non Comune", "#22A318FF")
#   RARE = ("Raro", "#098CDEFF")
#   VERY_RARE = ("Molto Raro", "#275EEBFF")
#   LEGENDARY = ("Leggendario", "#B411ABFF")
#   EXOTIC = ("Esotico", "#E8E409FF")

class Rarity(StrEnum):
    COMMON = "Comune"
    UNCOMMON = "Non Comune"
    RARE = "Raro"
    VERY_RARE = "Molto Raro"
    LEGENDARY = "Leggendario"
    EXOTIC = "Esotico"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not a Rarity"),
                params={"value": value},
            )

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

class ItemCategory(StrEnum):
    _PLACEHOLDER = "Categoria"
    ITEM = "Oggetto"
    EQUIPMENT = "Equipaggiamento"
    SPELL = "Incantesimo"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not a ItemCategory"),
                params={"value": value},
            )

    @classmethod
    def get_placeholder(cls):
        return cls._PLACEHOLDER

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

class EquipmentType(StrEnum):
    _PLACEHOLDER = "Tipo Equipaggiamento"
    ARMOR = "Armatura"
    WEAPON = "Arma"
    ADDON = "Addon"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not an EquipmentType"),
                params={"value": value},
            )

    @classmethod
    def get_placeholder(cls):
        return cls._PLACEHOLDER

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

class ArmorSlot(StrEnum):
    FULL_SET = "Set Completo"
    HEAD = "Testa"
    LEFT_SHOULDER = "Spalla SX"
    RIGHT_SHOULDER = "Spalla DX"
    LEFT_ARM = "Braccio SX"
    RIGHT_ARM = "Braccio DX"
    LEFT_FOREARM = "Avambraccio SX"
    RIGHT_FOREARM = "Avambraccio DX"
    LEFT_HAND = "Mano SX"
    RIGHT_HAND = "Mano DX"
    CHEST = "Petto"
    ABDOMEN = "Addome"
    BACK = "Schiena"
    LEFT_LEG = "Gamba SX"
    RIGHT_LEG = "Gamba DX"
    LEFT_KNEE = "Ginocchio SX"
    RIGHT_KNEE = "Ginocchio DX"
    LEFT_FOOT = "Piede SX"
    RIGHT_FOOT = "Piede DX"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not an ArmorSlot"),
                params={"value": value},
            )

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

class ArmorWeightCategory(StrEnum):
    LIGHT = "Leggero (+Mod Destrezza)"
    MEDIUM = "Medio (+Mod Destrezza MAX 2)"
    HEAVY = "Pesante (Nessun Modificatore)"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not an ArmorWeightCategory"),
                params={"value": value},
            )

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

class AddonSlot(StrEnum):
    NECKLACE = "Collana"
    MANTLE = "Mantello"
    BRACELET = "Bracciale"
    EARRING = "Orecchino"
    RING = "Anello"
    BACKPACK = "Zaino"
    BELT = "Cintura"
    BANDOLIER = "Bandoliera"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not an AddonSlot"),
                params={"value": value},
            )

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
