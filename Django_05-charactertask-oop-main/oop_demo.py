# OOP demo - Django-suz, sadə Python faylı
# İşə salmaq: py oop_demo.py

from characters.oop import Character, Warrior, Mage, Archer

# Character yaradırıq
base = Character("Base", 80, 10)
print(base)
print()

# inheritance
warrior = Warrior("Ali", 100, 20, 5)
mage = Mage("Vali", 70, 25, 30)
archer = Archer("Aysel", 80, 15, 5)

print(isinstance(warrior, Character))   # True
print(issubclass(Mage, Character))       # True
print(isinstance(archer, Warrior))       # False
print()

# __str__
print(warrior)
print()
print(mage)
print()
print(archer)
print()

# polymorphism - hamısı eyni siyahıda, attack() eyni cür çağırılır
characters = [warrior, mage, archer]
dummy = Character("Dummy", 500, 0)

for character in characters:
    damage = character.attack(dummy)
    print(f"{character.name} ({character.character_type}) -> {damage} damage")
print()

# take_damage, health azalır
victim = Character("Victim", 30, 5)
print("Health:", victim.health)
warrior.attack(victim)
print("Health:", victim.health)
print()

# __bool__ və __len__
print(bool(victim))     # True
mage.attack(victim)
print(bool(victim))     # False
print(len(victim))      # 0
print()

# __lt__ və __eq__
print(warrior < mage)   # True  (20 < 25)
print(mage < warrior)   # False
print(warrior == mage)  # False
print(warrior == Warrior("Ali", 100, 20, 5))    # True
print()

# __len__
print(len(warrior))     # health
print()

# __add__
team = warrior + mage
print(team)
print()

big_team = team + archer
print(big_team)
