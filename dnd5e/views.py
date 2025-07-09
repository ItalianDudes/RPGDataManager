from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from dnd5e.enums import ItemCategory, EquipmentType
from dnd5e.forms import ItemsForm, EditorItem
from dnd5e.models import Item


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'dnd5e/index.html')

def items(request: HttpRequest) -> HttpResponse:
    form = ItemsForm(request.POST)
    items_list = Item.objects.all().filter(visible=True)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        category = form.cleaned_data.get('category')
        if category:
            category = int(category)
        equipment_type = form.cleaned_data.get('equipment_type')
        if equipment_type:
            equipment_type = int(equipment_type)

        if name:
            items_list = items_list.filter(name__contains=name)
        if category and category in ItemCategory.values and category != ItemCategory.get_placeholder().value:
            items_list = items_list.filter(category=category)
            if category == ItemCategory.EQUIPMENT.value and equipment_type and equipment_type in EquipmentType.values and equipment_type != EquipmentType.get_placeholder().value:
                items_list = items_list.filter(equipment_type=equipment_type)

    return render(request, 'dnd5e/items.html', {'form': form, 'items': items_list})

def item(request: HttpRequest, item_id: int) -> HttpResponse:
    selected_item = Item.objects.filter(item_id=item_id).first()
    if selected_item is None:
        return HttpResponseNotFound('Oggetto non trovato.')

    if request.method == 'POST':
        form = EditorItem(request.POST)
        if form.is_valid():
            selected_item.name = form.cleaned_data['name']
            selected_item.rarity = form.cleaned_data['rarity']
            selected_item.weight = form.cleaned_data['weight']
            selected_item.cost_copper = form.cleaned_data['cost_copper']
            selected_item.description = form.cleaned_data['description']
            selected_item.save()
            return render(request, 'dnd5e/item.html', {'form': form, 'valid_form': True})
        else:
            return render(request, 'dnd5e/item.html', {'form': form, 'invalid_form': True})
    else:
        form = EditorItem(initial=selected_item.data_to_tuple())
        return render(request, 'dnd5e/item.html', {'form': form})

