from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.enums import IntegerChoices

#   COMMON = ("Comune", "#E0E0E0FF")
#   UNCOMMON = ("Non Comune", "#22A318FF")
#   RARE = ("Raro", "#098CDEFF")
#   VERY_RARE = ("Molto Raro", "#275EEBFF")
#   LEGENDARY = ("Leggendario", "#B411ABFF")
#   EXOTIC = ("Esotico", "#E8E409FF")


class Rarity(IntegerChoices):
    COMMON = 0, "Comune"
    UNCOMMON = 1, "Non Comune"
    RARE = 2, "Raro"
    VERY_RARE = 3, "Molto Raro"
    LEGENDARY = 4, "Leggendario"
    EXOTIC = 5, "Esotico"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not a Rarity"),
                params={"value": value},
            )

    @classmethod
    def choices_as_tuple(cls):
        return tuple(cls.choices)


class ItemCategory(IntegerChoices):
    _PLACEHOLDER = -1, "Categoria"
    ITEM = 0, "Oggetto"
    EQUIPMENT = 1, "Equipaggiamento"
    SPELL = 2, "Incantesimo"

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
    def choices_as_tuple(cls):
        return tuple(cls.choices)

    @classmethod
    def clean_choices(cls):
        return list(filter(lambda x: x != cls._PLACEHOLDER, cls.choices))

    @classmethod
    def clean_choices_as_tuple(cls):
        return tuple(list(filter(lambda x: x != cls._PLACEHOLDER, cls.choices)))


class EquipmentType(IntegerChoices):
    _PLACEHOLDER = -1, "Tipo Equipaggiamento"
    ARMOR = 0, "Armatura"
    WEAPON = 1, "Arma"
    ADDON = 2, "Addon"

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
    def choices_as_tuple(cls):
        return tuple(cls.choices)

    @classmethod
    def clean_choices(cls):
        return list(filter(lambda x: x != cls._PLACEHOLDER, cls.choices))

    @classmethod
    def clean_choices_as_tuple(cls):
        return tuple(list(filter(lambda x: x != cls._PLACEHOLDER, cls.choices)))


class ArmorSlot(IntegerChoices):
    FULL_SET = 0, "Set Completo"
    HEAD = 1, "Testa"
    LEFT_SHOULDER = 2, "Spalla"
    LEFT_ARM = 3, "Braccio"
    RIGHT_FOREARM = 4, "Avambraccio"
    LEFT_HAND = 5, "Mano"
    CHEST = 6, "Petto"
    ABDOMEN = 7, "Addome"
    BACK = 8, "Schiena"
    RIGHT_LEG = 9, "Gamba"
    LEFT_KNEE = 10, "Ginocchio"
    LEFT_FOOT = 11, "Piede"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not an ArmorSlot"),
                params={"value": value},
            )

    @classmethod
    def choices_as_tuple(cls):
        return tuple(cls.choices)


class ArmorWeightCategory(IntegerChoices):
    LIGHT = 0, "Leggero (+Mod Destrezza)"
    MEDIUM = 1, "Medio (+Mod Destrezza MAX 2)"
    HEAVY = 2, "Pesante (Nessun Modificatore)"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not an ArmorWeightCategory"),
                params={"value": value},
            )

    @classmethod
    def choices_as_tuple(cls):
        return tuple(cls.choices)


class AddonSlot(IntegerChoices):
    NECKLACE = 0, "Collana"
    MANTLE = 1, "Mantello"
    BRACELET = 2, "Bracciale"
    EARRING = 3, "Orecchino"
    RING = 4, "Anello"
    BACKPACK = 5, "Zaino"
    BELT = 6, "Cintura"
    BANDOLIER = 7, "Bandoliera"

    @classmethod
    def validate(cls, value):
        if value not in cls:
            raise ValidationError(
                _("%(value)s is not an AddonSlot"),
                params={"value": value},
            )

    @classmethod
    def choices_as_tuple(cls):
        return tuple(cls.choices)
