from django import forms
from django.forms import ChoiceField

from dnd5e.models import Item, Spell, Equipment, Weapon, Armor, Addon
from dnd5e.enums import Category, EquipmentType, Rarity, ArmorSlot, ArmorWeightCategory, AddonSlot


class ItemsForm(forms.Form):
    name = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        'placeholder': 'Nome Oggetto'
    }))
    category = forms.ChoiceField(
        required=False,
        label="",
        choices=Category.choices_as_tuple(),
        validators=[Category.form_validate]
    )
    equipment_type = forms.ChoiceField(
        required=False,
        label="",
        choices=EquipmentType.choices_as_tuple(),
        validators=[EquipmentType.form_validate]
    )


# TODO: Toggle editing
class EditorItem(forms.Form):
    name = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={
        'placeholder': 'Nome Oggetto'
    }))
    rarity = forms.ChoiceField(
        required=True,
        label="",
        choices=Rarity.choices_as_tuple(),
        validators=[Rarity.validate]
    )
    weight = forms.FloatField(
        required=True,
        label="Peso (KG)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Peso (KG)'
        })
    )
    cost_copper = forms.IntegerField(
        required=True,
        label="Costo (MR)",
        widget=forms.TextInput(attrs={
            'placeholder': 'Costo (MR)'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Descrizione'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_item = kwargs.get('initial', None)
        if not initial_item is None and isinstance(initial_item, Item):
            self.fields['name'].initial = initial_item.name
            self.fields['rarity'].initial = initial_item.rarity
            self.fields['weight'].initial = initial_item.weight
            self.fields['cost_copper'].initial = initial_item.cost_copper
            self.fields['description'].initial = initial_item.description


class EditorEquipment(EditorItem):
    ca_effect = forms.IntegerField(
        required=True,
        label="Effetto CA",
        step_size=1,
        widget=forms.TextInput(attrs={
            'placeholder': 'Effetto CA'
        })
    )
    life_effect = forms.IntegerField(
        required=True,
        label="Effetto Vita",
        step_size=1,
        widget=forms.TextInput(attrs={
            'placeholder': 'Effetto Vita'
        })
    )
    life_effect_perc = forms.FloatField(
        required=True,
        label="Effetto Vita%",
        widget=forms.TextInput(attrs={
            'placeholder': 'Effetto Vita%'
        })
    )
    load_effect = forms.IntegerField(
        required=True,
        label="Effetto Carico",
        step_size=1,
        widget=forms.TextInput(attrs={
            'placeholder': 'Effetto Carico'
        })
    )
    load_effect_perc = forms.FloatField(
        required=True,
        label="Effetto Carico%",
        widget=forms.TextInput(attrs={
            'placeholder': 'Effetto Carico%'
        })
    )
    other_effects = forms.CharField(
        required=False,
        label="Altri Effetti",
        widget=forms.Textarea(attrs={
            'placeholder': 'Altri Effetti'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_equipment = kwargs.get('initial', None)
        if not initial_equipment is None and isinstance(initial_equipment, Equipment):
            self.fields['ca_effect'].initial = initial_equipment.ca_effect
            self.fields['life_effect'].initial = initial_equipment.life_effect
            self.fields['life_effect_perc'].initial = initial_equipment.life_effect_perc
            self.fields['load_effect'].initial = initial_equipment.load_effect
            self.fields['load_effect_perc'].initial = initial_equipment.load_effect_perc
            self.fields['other_effects'].initial = initial_equipment.other_effects


class EditorArmor(EditorEquipment):
    armor_slot = ChoiceField(
        required=True,
        label="",
        choices=ArmorSlot.choices_as_tuple(),
        validators=[ArmorSlot.validate]
    )
    weight_category = ChoiceField(
        required=True,
        label="",
        choices=ArmorWeightCategory.choices_as_tuple(),
        validators=[ArmorWeightCategory.validate]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_armor = kwargs.get('initial', None)
        if not initial_armor is None and isinstance(initial_armor, Armor):
            self.fields['armor_slot'].initial = initial_armor.armor_slot
            self.fields['weight_category'].initial = initial_armor.weight_category


class EditorAddon(EditorEquipment):
    addon_slot = forms.ChoiceField(
        required=True,
        label="",
        choices=AddonSlot.choices_as_tuple(),
        validators=[AddonSlot.validate]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_addon = kwargs.get('initial', None)
        if not initial_addon is None and isinstance(initial_addon, Addon):
            self.fields['addon_slot'].initial = initial_addon.addon_slot


class EditorWeapon(EditorEquipment):
    weapon_category = forms.CharField(
        required=False,
        label="Categoria Arma",
        widget=forms.TextInput(attrs={
            'placeholder': 'Categoria Arma'
        })
    )
    properties = forms.CharField(
        required=False,
        label="Proprietà",
        widget=forms.Textarea(attrs={
            'placeholder': 'Proprietà'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_weapon = kwargs.get('initial', None)
        if not initial_weapon is None and isinstance(initial_weapon, Weapon):
            self.fields['weapon_category'].initial = initial_weapon.weapon_category
            self.fields['properties'].initial = initial_weapon.properties


class EditorSpell(EditorItem):
    level = forms.IntegerField(
        required=True,
        label="Livello",
        min_value=0,
        max_value=9,
        step_size=1,
        widget=forms.TextInput(attrs={
            'placeholder': 'Livello'
        })
    )
    spell_type = forms.CharField(
        required=True,
        label="Tipo Incantesimo",
        max_length=64,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tipo Incantesimo'
        })
    )
    cast_time = forms.CharField(
        required=True,
        label="Tempo di Lancio",
        max_length=64,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tempo di Lancio'
        })
    )
    range = forms.CharField(
        required=True,
        label="Portata",
        max_length=64,
        widget=forms.TextInput(attrs={
            'placeholder': 'Portata'
        })
    )
    components = forms.CharField(
        required=True,
        label="Componenti",
        max_length=64,
        widget=forms.TextInput(attrs={
            'placeholder': 'Componenti'
        })
    )
    duration = forms.CharField(
        required=True,
        label="Durata",
        widget=forms.TextInput(attrs={
            'placeholder': 'Durata'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_spell = kwargs.get('initial', None)
        if not initial_spell is None and isinstance(initial_spell, Spell):
            self.fields['level'].initial = initial_spell.level
            self.fields['spell_type'].initial = initial_spell.spell_type
            self.fields['cast_time'].initial = initial_spell.cast_time
            self.fields['range'].initial = initial_spell.range
            self.fields['components'].initial = initial_spell.components
            self.fields['duration'].initial = initial_spell.duration
