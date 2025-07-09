from typing import Any

from django.db import models

from dnd5e.enums import ArmorWeightCategory, AddonSlot, ItemCategory, EquipmentType, Rarity, ArmorSlot


class Item(models.Model):
    item_id = models.IntegerField(primary_key=True)
    base64_image = models.TextField(null=True, blank=True)
    image_extension = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=256, null=False, blank=False, unique=True)
    category = models.CharField(choices=ItemCategory.clean_choices_as_tuple(), validators=[ItemCategory.validate])
    rarity = models.CharField(choices=Rarity.choices_as_tuple(), default=Rarity.COMMON, validators=[Rarity.validate])
    weight = models.FloatField(default=0, null=False, blank=False)
    cost_copper = models.IntegerField(default=0, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    visible = models.BooleanField(default=True)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        Rarity.validate(self.rarity)
        ItemCategory.validate(self.category)

    def data_to_tuple(self):
        return {
            'name': self.name,
            'category': self.category,
            'rarity': self.rarity,
            'weight': self.weight,
            'cost_copper': self.cost_copper,
            'description': self.description,
        }


class Equipment(Item):
    equipment_id = models.IntegerField(primary_key=True)
    type = models.CharField(choices=EquipmentType.clean_choices_as_tuple(), validators=[EquipmentType.validate])
    ca_effect = models.IntegerField(null=False, blank=False, default=0)
    life_effect = models.IntegerField(null=False, blank=False, default=0)
    life_effect_perc = models.FloatField(null=False, blank=False, default=0)
    load_effect = models.IntegerField(null=False, blank=False, default=0)
    load_effect_perc = models.FloatField(null=False, blank=False, default=0)
    other_effects = models.TextField(null=False, blank=True)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        EquipmentType.validate(self.type)

class Armor(Equipment):
    armor_id = models.IntegerField(primary_key=True)
    armor_slot = models.CharField(choices=ArmorSlot.choices_as_tuple(), validators=[ArmorSlot.validate])
    weight_category = models.CharField(choices=ArmorWeightCategory.choices_as_tuple(), validators=[ArmorWeightCategory.validate])

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        ArmorSlot.validate(self.armor_slot)
        ArmorWeightCategory.validate(self.weight_category)

class Addon(Equipment):
    addon_id = models.IntegerField(primary_key=True)
    addon_slot = models.CharField(choices=AddonSlot.choices_as_tuple(), validators=[AddonSlot.validate])

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        AddonSlot.validate(self.addon_slot)

class Weapon(Equipment):
    weapon_id = models.IntegerField(primary_key=True)
    weapon_category = models.CharField(null=False, blank=True, max_length=64)
    properties = models.TextField(null=False, blank=True)

class Spell(Item):
    spell_id = models.IntegerField(primary_key=True)
    level = models.IntegerField(null=False, blank=False, default=0)
    spell_type = models.CharField(null=False, blank=False, max_length=32)
    cast_time = models.CharField(null=False, blank=False, max_length=64)
    range = models.CharField(null=False, blank=False, max_length=64)
    components = models.CharField(null=False, blank=False, max_length=64)
    duration = models.CharField(null=False, blank=False, max_length=64)