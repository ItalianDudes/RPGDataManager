from django import forms

from dnd5e.enums import ItemCategory, EquipmentType


class ItemsForm(forms.Form):
    name = forms.CharField(required=False, help_text='Nome Oggetto')
    item_category = forms.ChoiceField(
        required=False,
        choices=[(item_cat.__str__()) for item_cat in ItemCategory]
    )
    equipment_type = forms.ChoiceField(
        required=False,
        choices=[(eq_type.__str__()) for eq_type in EquipmentType]
    )