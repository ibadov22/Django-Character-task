from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render

from . import demo
from .forms import CharacterForm, AttackForm
from .models import CharacterRecord


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'characters/home.html')


def characters_list(request: HttpRequest) -> HttpResponse:
    items = []
    for record in CharacterRecord.objects.all():
        character = record.to_object()      # Warrior / Mage / Archer obyekti
        items.append({
            'id': record.pk,
            'name': character.name,
            'type': character.character_type,
            'health': character.health,
            'attack_power': character.attack_power,
            'is_alive': bool(character),    # __bool__
            'info': character.get_info(),
        })
    return render(request, 'characters/characters_list.html', {'items': items})


def character_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, f"{record.name} uğurla yaradıldı")
            return redirect('characters:characters_list')
    else:
        form = CharacterForm()

    return render(request, 'characters/character_create.html', {'form': form})


def character_attack(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AttackForm(request.POST)
        if form.is_valid():
            attacker_record = form.cleaned_data['attacker']
            target_record = form.cleaned_data['target']

            attacker = attacker_record.to_object()
            target = target_record.to_object()

            # POLYMORPHISM: attacker hansı tipdədirsə, onun attack() metodu işləyir
            damage = attacker.attack(target)

            attacker_record.update_from_object(attacker)
            target_record.update_from_object(target)

            messages.success(
                request,
                f"{attacker.name} ({attacker.character_type}) attacked "
                f"{target.name} ({target.character_type})"
            )
            messages.info(request, f"{target.name} lost {damage} health")
            if not target:      # __bool__
                messages.warning(request, f"{target.name} öldü")
            return redirect('characters:character_attack')
    else:
        form = AttackForm()

    return render(request, 'characters/character_attack.html', {'form': form})


def oop_demo(request: HttpRequest) -> HttpResponse:
    return render(request, 'characters/oop_demo.html', {'sections': demo.run_demo()})
