from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib import messages

from dnd5e.enums import Category, EquipmentType
from dnd5e.forms import ItemsForm, EditorItem
from dnd5e.models import Item, Equipment


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'dnd5e/index.html')

def items(request: HttpRequest) -> HttpResponse:
    form = ItemsForm(request.POST)
    action = request.POST.get('action')
    items_list = Item.objects.all().filter(visible=True)

    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data.get('name')

        category = form.cleaned_data.get('category')
        if not category is None:
            try:
                category = int(category)
            except ValueError:
                return HttpResponseBadRequest('Tipo Equipaggiamento non valido')

        equipment_type = form.cleaned_data.get('equipment_type')
        if not equipment_type is None:
            try:
                equipment_type = int(equipment_type)
            except ValueError:
                return HttpResponseBadRequest('Tipo Equipaggiamento non valido')

        if action == 'new':
            if not category is None and category in Category.values and category != Category.get_placeholder().value: # Valid Category
                request.session['category'] = category
                if category == Category.EQUIPMENT.value: # Category = EquipmentType
                    if not equipment_type is None and equipment_type in EquipmentType.values and equipment_type != EquipmentType.get_placeholder().value: # Valid Category and EquipmentType
                        request.session['equipment_type'] = equipment_type
                        return redirect('new')
                    else: # Valid Category but invalid EquipmentType
                        messages.error(request, 'Categoria valida, Tipo Equipaggiamento non valido, inserire un Tipo Equipaggiamento valido.')
                else: # Valid Non-Equipment item
                    return redirect('new')
            else: # Invalid Category
                messages.error(request, 'Categoria non valida, inserire una Categoria valida.')

        elif action == 'search':
            if name:
                items_list = items_list.filter(name__contains=name)
            if not category is None and category in Category.values and category != Category.get_placeholder().value:
                items_list = items_list.filter(category=category)
                if category == Category.EQUIPMENT.value and not equipment_type is None and equipment_type in EquipmentType.values and equipment_type != EquipmentType.get_placeholder().value:
                    items_list = Equipment.objects.all().filter(equipment_type=equipment_type)

    return render(request, 'dnd5e/items.html', {'form': form, 'items': items_list})

def new(request: HttpRequest) -> HttpResponse:
    item_id = request.session.get('item_id', None)
    category = request.session.get('category', None)
    equipment_type = request.session.get('equipment_type', None)
    print(f'REQMETHOD: {request.method}')
    print(f'ITEM_ID: {item_id}')
    print(f'CATEGORY: {category}')
    print(f'EQTYPE: {equipment_type}')

    if item_id is None: # New
        if request.method == 'POST': # Form Received
            form = EditorItem(request.POST)
            if form.is_valid(): # Valid Form
                new_item = Item(
                    name=form.cleaned_data['name'],
                    category=Category.ITEM,
                    rarity=form.cleaned_data['rarity'],
                    weight=form.cleaned_data['weight'],
                    cost_copper=form.cleaned_data['cost_copper'],
                    description=form.cleaned_data['description']
                )
                new_item.save()
                messages.success(request, 'Salvataggio avvenuto con successo!')
                return redirect('edit', new_item.item_id)
            else: # Invalid Form
                messages.error(request, "Form non valido, controllare i dati inseriti.")
                return render(request, 'dnd5e/item.html', {'form': form})
        else: # Initial Get
            return render(request, 'dnd5e/item.html', {'form': EditorItem(request.POST)})
    else: # Edit
        return redirect('edit', item_id)

def edit(request: HttpRequest, item_id: int) -> HttpResponse: #Only works with Item... for the moment
    selected_item = Item.objects.filter(item_id=item_id).first()
    if selected_item is None:
        return HttpResponseNotFound('Oggetto non trovato.')

    if selected_item.category != Category.ITEM:
        return HttpResponseServerError('Edit al momento disponibile solo per gli oggetti.')

    if request.method == 'POST':
        form = EditorItem(request.POST)
        if form.is_valid():
            selected_item.name = form.cleaned_data['name']
            selected_item.rarity = form.cleaned_data['rarity']
            selected_item.weight = form.cleaned_data['weight']
            selected_item.cost_copper = form.cleaned_data['cost_copper']
            selected_item.description = form.cleaned_data['description']
            selected_item.save()
            messages.success(request,'Salvataggio avvenuto con successo!')
        else:
            messages.error(request, "Form non valido, controllare i dati inseriti.")
        return render(request, 'dnd5e/item.html', {'form': form})
    else:
        form = EditorItem(initial=selected_item.data_to_tuple())
        return render(request, 'dnd5e/item.html', {'form': form})