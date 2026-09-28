from .oop import Character, Warrior, Mage, Archer


# Bu funksiya OOP anlayışlarını real obyektlərlə işlədir.
# Nəticə browser-də göstərilir: /characters/demo/
# (Eyni nümunənin sadə Python versiyası: oop_demo.py)

def run_demo():
    sections = []

    def add(title, code, result):
        sections.append({'title': title, 'code': code, 'result': str(result)})

    # obyektlər
    base = Character("Base", 80, 10)
    warrior = Warrior("Ali", 100, 20, 5)
    mage = Mage("Vali", 70, 25, 30)
    archer = Archer("Aysel", 80, 15, 5)

    # ---------- Inheritance ----------
    add("Inheritance",
        "isinstance(warrior, Character)\nissubclass(Mage, Character)\nisinstance(archer, Warrior)",
        f"{isinstance(warrior, Character)}\n{issubclass(Mage, Character)}\n{isinstance(archer, Warrior)}")

    # ---------- __str__ ----------
    add("__str__ (Character)", "print(base)", base)
    add("__str__ (Warrior)", "print(warrior)", warrior)
    add("__str__ (Mage)", "print(mage)", mage)
    add("__str__ (Archer)", "print(archer)", archer)

    # ---------- Polymorphism ----------
    characters = [warrior, mage, archer]
    dummy = Character("Dummy", 500, 0)
    lines = []
    for character in characters:
        damage = character.attack(dummy)
        lines.append(f"{character.name} ({character.character_type}) -> {damage} damage")
    add("Polymorphism",
        "characters = [warrior, mage, archer]\nfor character in characters:\n    character.attack(dummy)",
        "\n".join(lines))

    # ---------- take_damage ----------
    victim = Character("Victim", 30, 5)
    before = victim.health
    lost = warrior.attack(victim)
    add("take_damage / health azalır",
        "warrior.attack(victim)",
        f"Health before: {before}\nLost: {lost}\nHealth after: {victim.health}")

    # ---------- __bool__ ----------
    add("__bool__ (sağdır)", "bool(victim)", bool(victim))
    mage.attack(victim)     # victim ölür
    add("__bool__ (ölüb)",
        "mage.attack(victim)\nbool(victim)\nlen(victim)",
        f"{bool(victim)}\n{len(victim)}")

    # ---------- __lt__ / __eq__ ----------
    fresh_warrior = Warrior("Ali", 100, 20, 5)
    add("__lt__ (attack_power)",
        "warrior < mage\nmage < warrior",
        f"{warrior < mage}  ({warrior.attack_power} < {mage.attack_power})\n"
        f"{mage < warrior}  ({mage.attack_power} < {warrior.attack_power})")
    add("__eq__",
        "warrior == mage\nfresh_warrior == Warrior('Ali', 100, 20, 5)",
        f"{warrior == mage}\n{fresh_warrior == Warrior('Ali', 100, 20, 5)}")

    # ---------- __len__ ----------
    add("__len__ (health)", "len(fresh_warrior)", len(fresh_warrior))

    # ---------- __add__ ----------
    team = fresh_warrior + Mage("Vali", 70, 25, 30)
    add("__add__ (Character + Character)", "team = warrior + mage\nprint(team)", team)
    big_team = team + Archer("Aysel", 80, 15, 5)
    add("__add__ (Team + Character)", "big_team = team + archer\nprint(big_team)", big_team)

    return sections
