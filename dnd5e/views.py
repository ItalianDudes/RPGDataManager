from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from dnd5e.enums import ItemCategory, EquipmentType
from dnd5e.forms import ItemsForm
from dnd5e.models import Item


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'dnd5e/index.html')

def items(request: HttpRequest) -> HttpResponse:
    form = ItemsForm(request.POST)
    items_list = Item.objects.all().filter(visible=True)

    # FUNZIONA, PARTI DA QUI!!
    print(ItemCategory.choices)
    print(ItemCategory.values)
    print(ItemCategory.names)
    print(ItemCategory.labels)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        category = form.cleaned_data.get('category')
        equipment_type = form.cleaned_data.get('equipment_type')

        print(f"CATEGORY: {category}")
        print(f"CATEGORY CHOICES: {ItemCategory.choices}")

        if name:
            items_list = items_list.filter(name__contains=name)
        if category and category in ItemCategory.choices and category != ItemCategory.get_placeholder():
            items_list = items_list.filter(category=category)
            if category == ItemCategory.EQUIPMENT and equipment_type and equipment_type in EquipmentType.choices and equipment_type != EquipmentType.get_placeholder():
                items_list = items_list.filter(equipment_type=equipment_type)

    return render(request, 'dnd5e/items.html', {'form': form, 'items': items_list})

def item(request: HttpRequest, item_id: int) -> HttpResponse:
    selected_item = Item.objects.filter(item_id=item_id).first()
    if selected_item:
        return render(request, 'dnd5e/item.html', {'item': selected_item})
    else:
        return HttpResponseNotFound('Item not found.')