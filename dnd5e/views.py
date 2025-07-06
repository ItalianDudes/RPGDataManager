from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from dnd5e.enums import ItemCategory
from dnd5e.forms import ItemsForm
from dnd5e.models import Item


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'dnd5e/index.html')

def items(request: HttpRequest) -> HttpResponse:
    form = ItemsForm(request.GET)
    items_list = Item.objects.all().filter(visible=True)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        item_category = form.cleaned_data.get('item_category')
        equipment_type = form.cleaned_data.get('equipment_type')

        if name:
            items_list = items_list.filter(name__contains=name)
        if item_category:
            items_list = items_list.filter(item_category=item_category)
        if item_category == ItemCategory.EQUIPMENT and equipment_type:
            items_list = items_list.filter(equipment_type=equipment_type)

    print(items_list.count())

    return render(request, 'dnd5e/items.html', {'form': form, 'items': items_list})
