from django import forms

from dnd5e.models import Item
from dnd5e.enums import Category, EquipmentType, Rarity


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
