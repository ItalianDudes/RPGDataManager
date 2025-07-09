from django import forms

from dnd5e.enums import ItemCategory, EquipmentType


class ItemsForm(forms.Form):
    name = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        'placeholder': 'Nome Oggetto'
    }))
    category = forms.ChoiceField(
        required=False,
        choices=ItemCategory.choices_as_tuple(),
        label="",
        validators=[ItemCategory.validate]
    )
    equipment_type = forms.ChoiceField(
        required=False,
        choices=EquipmentType.choices_as_tuple(),
        label="",
        validators=[EquipmentType.validate]
    )