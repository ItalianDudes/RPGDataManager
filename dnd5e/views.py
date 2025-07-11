from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages

from dnd5e.enums import Category, EquipmentType
from dnd5e.forms import ItemsForm, EditorItem, EditorArmor, EditorSpell, EditorAddon, EditorWeapon
from dnd5e.models import Item, Equipment, Spell, Armor, Addon, Weapon


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

    if item_id is None: # New
        if request.method == 'POST': # Form Received

            if category == Category.ITEM:  # Item
                form = EditorItem(request.POST)
                if form.is_valid():  # Valid Form
                    new_weapon = Item(
                        name=form.cleaned_data['name'],
                        category=Category.ITEM,
                        rarity=form.cleaned_data['rarity'],
                        weight=form.cleaned_data['weight'],
                        cost_copper=form.cleaned_data['cost_copper'],
                        description=form.cleaned_data['description']
                    )
                    new_weapon.save()
                    messages.success(request, 'Salvataggio oggetto avvenuto con successo!')
                    return redirect('edit', new_weapon.item_id)
                else:
                    messages.error(request, "Form non valido, controllare i dati inseriti.")
                    return render(request, 'dnd5e/item.html', {'form': form})

            elif category == Category.SPELL:  # Spell
                form = EditorSpell(request.POST)
                if form.is_valid():  # Valid Form
                    new_spell = Spell(
                        name=form.cleaned_data['name'],
                        category=Category.SPELL,
                        rarity=form.cleaned_data['rarity'],
                        weight=form.cleaned_data['weight'],
                        cost_copper=form.cleaned_data['cost_copper'],
                        description=form.cleaned_data['description'],
                        level=form.cleaned_data['level'],
                        spell_type=form.cleaned_data['spell_type'],
                        cast_time=form.cleaned_data['cast_time'],
                        range=form.cleaned_data['range'],
                        components=form.cleaned_data['components'],
                        duration=form.cleaned_data['duration']
                    )
                    new_spell.save()
                    messages.success(request, 'Salvataggio incantesimo avvenuto con successo!')
                    return redirect('edit', new_spell.item_id)
                else:
                    messages.error(request, "Form non valido, controllare i dati inseriti.")
                    return render(request, 'dnd5e/spell.html', {'form': form})

            elif category == Category.EQUIPMENT:  # Equipment
                if equipment_type == EquipmentType.ARMOR:  # Armor
                    form = EditorArmor(request.POST)
                    if form.is_valid():  # Valid Form
                        new_weapon = Armor(
                            name=form.cleaned_data['name'],
                            category=Category.EQUIPMENT,
                            rarity=form.cleaned_data['rarity'],
                            weight=form.cleaned_data['weight'],
                            cost_copper=form.cleaned_data['cost_copper'],
                            description=form.cleaned_data['description'],
                            equipment_type=EquipmentType.ARMOR,
                            ca_effect=form.cleaned_data['ca_effect'],
                            life_effect=form.cleaned_data['life_effect'],
                            life_effect_perc=form.cleaned_data['life_effect_perc'],
                            load_effect=form.cleaned_data['load_effect'],
                            load_effect_perc=form.cleaned_data['load_effect_perc'],
                            other_effects=form.cleaned_data['other_effects'],
                            armor_slot=form.cleaned_data['armor_slot'],
                            weight_category=form.cleaned_data['weight_category']
                        )
                        new_weapon.save()
                        messages.success(request, 'Salvataggio armatura avvenuto con successo!')
                        return redirect('edit', new_weapon.item_id)
                    else:
                        messages.error(request, "Form non valido, controllare i dati inseriti.")
                        return render(request, 'dnd5e/armor.html', {'form': form})

                elif equipment_type == EquipmentType.ADDON:  # Addon
                    form = EditorAddon(request.POST)
                    if form.is_valid():  # Valid Form
                        new_weapon = Addon(
                            name=form.cleaned_data['name'],
                            category=Category.EQUIPMENT,
                            rarity=form.cleaned_data['rarity'],
                            weight=form.cleaned_data['weight'],
                            cost_copper=form.cleaned_data['cost_copper'],
                            description=form.cleaned_data['description'],
                            equipment_type=EquipmentType.ADDON,
                            ca_effect=form.cleaned_data['ca_effect'],
                            life_effect=form.cleaned_data['life_effect'],
                            life_effect_perc=form.cleaned_data['life_effect_perc'],
                            load_effect=form.cleaned_data['load_effect'],
                            load_effect_perc=form.cleaned_data['load_effect_perc'],
                            other_effects=form.cleaned_data['other_effects'],
                            addon_slot=form.cleaned_data['addon_slot']
                        )
                        new_weapon.save()
                        messages.success(request, 'Salvataggio addon avvenuto con successo!')
                        return redirect('edit', new_weapon.item_id)
                    messages.error(request, "Form non valido, controllare i dati inseriti.")
                    return render(request, 'dnd5e/addon.html', {'form': form})

                elif equipment_type == EquipmentType.WEAPON:  # Weapon
                    form = EditorWeapon(request.POST)
                    if form.is_valid():  # Valid Form
                        new_weapon = Weapon(
                            name=form.cleaned_data['name'],
                            category=Category.EQUIPMENT,
                            rarity=form.cleaned_data['rarity'],
                            weight=form.cleaned_data['weight'],
                            cost_copper=form.cleaned_data['cost_copper'],
                            description=form.cleaned_data['description'],
                            equipment_type=EquipmentType.WEAPON,
                            ca_effect=form.cleaned_data['ca_effect'],
                            life_effect=form.cleaned_data['life_effect'],
                            life_effect_perc=form.cleaned_data['life_effect_perc'],
                            load_effect=form.cleaned_data['load_effect'],
                            load_effect_perc=form.cleaned_data['load_effect_perc'],
                            other_effects=form.cleaned_data['other_effects'],
                            weapon_category=form.cleaned_data['weapon_category'],
                            properties=form.cleaned_data['properties']
                        )
                        new_weapon.save()
                        messages.success(request, 'Salvataggio arma avvenuto con successo!')
                        return redirect('edit', new_weapon.item_id)
                    messages.error(request, "Form non valido, controllare i dati inseriti.")
                    return render(request, 'dnd5e/weapon.html', {'form': form})

                else:  # Invalid EquipmentType
                    return HttpResponseBadRequest('Tipo Equipaggiamento non valido.')
            else:  # Invalid Category
                return HttpResponseBadRequest('Categoria non valida.')
        else: # Initial Get
            if category == Category.ITEM: # Item
                return render(request, 'dnd5e/item.html', {'form': EditorItem(request.POST)})
            elif category == Category.SPELL: # Spell
                return render(request, 'dnd5e/spell.html', {'form': EditorSpell(request.POST)})
            elif category == Category.EQUIPMENT: # Equipment
                if equipment_type == EquipmentType.ARMOR: # Armor
                    return render(request, 'dnd5e/armor.html', {'form': EditorArmor(request.POST)})
                elif equipment_type == EquipmentType.ADDON: # Addon
                    return render(request, 'dnd5e/addon.html', {'form': EditorAddon(request.POST)})
                elif equipment_type == EquipmentType.WEAPON: # Weapon
                    return render(request, 'dnd5e/weapon.html', {'form': EditorWeapon(request.POST)})
                else: # Invalid EquipmentType
                    return HttpResponseBadRequest('Tipo Equipaggiamento non valido.')
            else: # Invalid Category
                return HttpResponseBadRequest('Categoria non valida.')
    else: # Edit
        return redirect('edit', item_id)


# TODO: PROBLEMA: la new salva correttamente i dati sul DB, ma la edit anche se carica il template corretto non carica in esso i dati

def edit(request: HttpRequest, item_id: int) -> HttpResponse: #Only works with Item... for the moment
    selected_item = Item.objects.filter(item_id=item_id).first()
    if selected_item is None:
        return HttpResponseNotFound('Oggetto non trovato.')

    category = selected_item.category

    if request.method == 'POST': # Form Received
        if category == Category.ITEM:
            form = EditorItem(request.POST)
            if form.is_valid():
                selected_item.name = form.cleaned_data['name']
                selected_item.rarity = form.cleaned_data['rarity']
                selected_item.weight = form.cleaned_data['weight']
                selected_item.cost_copper = form.cleaned_data['cost_copper']
                selected_item.description = form.cleaned_data['description']
                selected_item.save()
                messages.success(request,'Salvataggio oggetto avvenuto con successo!')
            else:
                messages.error(request, "Form non valido, controllare i dati inseriti.")
            return render(request, 'dnd5e/item.html', {'form': form})

        elif category == Category.SPELL:
            form = EditorSpell(request.POST)
            if form.is_valid():
                selected_item.name = form.cleaned_data['name']
                selected_item.rarity = form.cleaned_data['rarity']
                selected_item.weight = form.cleaned_data['weight']
                selected_item.cost_copper = form.cleaned_data['cost_copper']
                selected_item.description = form.cleaned_data['description']
                selected_item.level = form.cleaned_data['level']
                selected_item.spell_type = form.cleaned_data['spell_type']
                selected_item.cast_time = form.cleaned_data['cast_time']
                selected_item.range = form.cleaned_data['range']
                selected_item.components = form.cleaned_data['components']
                selected_item.duration = form.cleaned_data['duration']
                selected_item.save()
                messages.success(request,'Salvataggio incantesimo avvenuto con successo!')
            else:
                messages.error(request, "Form non valido, controllare i dati inseriti.")
            return render(request, 'dnd5e/spell.html', {'form': form})

        elif category == Category.EQUIPMENT:
            selected_item = Equipment.objects.all().filter(item_id=item_id).first()
            equipment_type = selected_item.equipment_type
            if equipment_type == EquipmentType.ARMOR:
                form = EditorArmor(request.POST)
                if form.is_valid():
                    selected_item.name = form.cleaned_data['name']
                    selected_item.rarity = form.cleaned_data['rarity']
                    selected_item.weight = form.cleaned_data['weight']
                    selected_item.cost_copper = form.cleaned_data['cost_copper']
                    selected_item.description = form.cleaned_data['description']
                    selected_item.ca_effect = form.cleaned_data['ca_effect']
                    selected_item.life_effect = form.cleaned_data['life_effect']
                    selected_item.life_effect_perc = form.cleaned_data['life_effect_perc']
                    selected_item.load_effect = form.cleaned_data['load_effect']
                    selected_item.load_effect_perc = form.cleaned_data['load_effect_perc']
                    selected_item.other_effects = form.cleaned_data['other_effects']
                    selected_item.armor_slot = form.cleaned_data['armor_slot']
                    selected_item.weight_category = form.cleaned_data['weight_category']
                    selected_item.save()
                    messages.success(request, 'Salvataggio armatura avvenuto con successo!')
                else:
                    messages.error(request, "Form non valido, controllare i dati inseriti.")
                return render(request, 'dnd5e/armor.html', {'form': form})

            elif equipment_type == EquipmentType.ADDON:
                form = EditorAddon(request.POST)
                if form.is_valid():
                    selected_item.name = form.cleaned_data['name']
                    selected_item.rarity = form.cleaned_data['rarity']
                    selected_item.weight = form.cleaned_data['weight']
                    selected_item.cost_copper = form.cleaned_data['cost_copper']
                    selected_item.description = form.cleaned_data['description']
                    selected_item.ca_effect = form.cleaned_data['ca_effect']
                    selected_item.life_effect = form.cleaned_data['life_effect']
                    selected_item.life_effect_perc = form.cleaned_data['life_effect_perc']
                    selected_item.load_effect = form.cleaned_data['load_effect']
                    selected_item.load_effect_perc = form.cleaned_data['load_effect_perc']
                    selected_item.other_effects = form.cleaned_data['other_effects']
                    selected_item.addon_slot = form.cleaned_data['addon_slot']
                    selected_item.save()
                    messages.success(request, 'Salvataggio addon avvenuto con successo!')
                else:
                    messages.error(request, "Form non valido, controllare i dati inseriti.")
                return render(request, 'dnd5e/addon.html', {'form': form})

            elif equipment_type == EquipmentType.WEAPON:
                form = EditorWeapon(request.POST)
                if form.is_valid():
                    selected_item.name = form.cleaned_data['name']
                    selected_item.rarity = form.cleaned_data['rarity']
                    selected_item.weight = form.cleaned_data['weight']
                    selected_item.cost_copper = form.cleaned_data['cost_copper']
                    selected_item.description = form.cleaned_data['description']
                    selected_item.ca_effect = form.cleaned_data['ca_effect']
                    selected_item.life_effect = form.cleaned_data['life_effect']
                    selected_item.life_effect_perc = form.cleaned_data['life_effect_perc']
                    selected_item.load_effect = form.cleaned_data['load_effect']
                    selected_item.load_effect_perc = form.cleaned_data['load_effect_perc']
                    selected_item.other_effects = form.cleaned_data['other_effects']
                    selected_item.weapon_category = form.cleaned_data['weapon_category']
                    selected_item.properties = form.cleaned_data['properties']
                    selected_item.save()
                    messages.success(request, 'Salvataggio arma avvenuto con successo!')
                else:
                    messages.error(request, "Form non valido, controllare i dati inseriti.")
                return render(request, 'dnd5e/weapon.html', {'form': form})

            else:
                return HttpResponseBadRequest('Tipo Equipaggiamento non valido.')
        else:
            return HttpResponseBadRequest('Categoria non valida.')

    else: # Initial Get
        if category == Category.ITEM:  # Item
            return render(request, 'dnd5e/item.html', {'form': EditorItem(initial=selected_item.data_to_tuple())})
        elif category == Category.SPELL:  # Spell
            return render(request, 'dnd5e/spell.html', {'form': EditorSpell(initial=selected_item.data_to_tuple())})
        elif category == Category.EQUIPMENT:  # Equipment
            selected_item = Equipment.objects.all().filter(item_id=item_id).first()
            equipment_type = selected_item.equipment_type
            if equipment_type == EquipmentType.ARMOR:  # Armor
                return render(request, 'dnd5e/armor.html', {'form': EditorArmor(initial=selected_item.data_to_tuple())})
            elif equipment_type == EquipmentType.ADDON:  # Addon
                return render(request, 'dnd5e/addon.html', {'form': EditorAddon(initial=selected_item.data_to_tuple())})
            elif equipment_type == EquipmentType.WEAPON:  # Weapon
                return render(request, 'dnd5e/weapon.html', {'form': EditorWeapon(initial=selected_item.data_to_tuple())})
            else:  # Invalid EquipmentType
                return HttpResponseBadRequest('Tipo Equipaggiamento non valido.')
        else:  # Invalid Category
            return HttpResponseBadRequest('Categoria non valida.')
