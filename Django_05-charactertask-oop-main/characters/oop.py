# ============================================================
# Python OOP hissəsi (Django-dan asılı deyil)
# Character -> Warrior, Mage, Archer
# ============================================================


class Character:
    # class attribute -> hər class öz tipini bu adla saxlayır
    character_type = "Character"

    def __init__(self, name, health, attack_power):
        self.name = name                                # public
        self.__health = health if health > 0 else 0     # private
        self.attack_power = attack_power                # public

    # ---------- encapsulation ----------
    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health if health > 0 else 0

    # ---------- əsas əməliyyatlar ----------
    def attack(self, target):
        # 1. başqa personaja hücum et
        if not self or not target:      # __bool__ işləyir
            return 0
        damage = self.attack_power
        return target.take_damage(damage)

    def take_damage(self, damage):
        # 2. zərər al (health 0-dan aşağı düşmür)
        damage = max(damage, 0)
        lost = min(damage, self.health)
        self.health = self.health - lost
        return lost

    def get_info(self):
        # 3. özü haqqında məlumat
        return (f"{self.character_type}: {self.name}\n"
                f"Health: {self.health}\n"
                f"Attack Power: {self.attack_power}")

    def get_special(self):
        # Warrior / Mage / Archer öz xüsusi dəyərini qaytarır
        return 0

    # ---------- magic methods ----------
    def __str__(self):
        return self.get_info()

    def __add__(self, other):
        # warrior + mage -> Team
        return Team([self, other])

    def __lt__(self, other):
        # attack_power-ə görə müqayisə: zəif personaj "kiçikdir"
        if not isinstance(other, Character):
            return NotImplemented
        return self.attack_power < other.attack_power

    def __eq__(self, other):
        # ad, tip, health və attack_power eynidirsə -> bərabərdir
        if not isinstance(other, Character):
            return NotImplemented
        return (self.name == other.name
                and self.character_type == other.character_type
                and self.health == other.health
                and self.attack_power == other.attack_power)

    def __len__(self):
        # len(character) -> health
        return self.health

    def __bool__(self):
        # sağdırsa True, ölübsə False
        return self.health > 0


class Warrior(Character):
    character_type = "Warrior"

    def __init__(self, name, health, attack_power, defense):
        super().__init__(name, health, attack_power)
        self.defense = defense

    def attack(self, target):
        # fiziki hücum: qılınc zərbəsi
        if not self or not target:
            return 0
        damage = self.attack_power + 5
        return target.take_damage(damage)

    def take_damage(self, damage):
        # Warrior zərəri defense qədər azaldır
        damage = max(damage - self.defense, 0)
        return super().take_damage(damage)

    def get_info(self):
        return f"{super().get_info()}\nDefense: {self.defense}"

    def get_special(self):
        return self.defense


class Mage(Character):
    character_type = "Mage"

    def __init__(self, name, health, attack_power, mana):
        super().__init__(name, health, attack_power)
        self.mana = mana

    def attack(self, target):
        # magic hücum: 10 mana xərcləyir, zərər 2 dəfə güclüdür
        if not self or not target:
            return 0
        if self.mana >= 10:
            self.mana -= 10
            damage = self.attack_power * 2
        else:
            damage = self.attack_power // 2     # mana bitib, sadəcə əsa ilə vurur
        return target.take_damage(damage)

    def get_info(self):
        return f"{super().get_info()}\nMana: {self.mana}"

    def get_special(self):
        return self.mana


class Archer(Character):
    character_type = "Archer"

    def __init__(self, name, health, attack_power, arrows):
        super().__init__(name, health, attack_power)
        self.arrows = arrows

    def attack(self, target):
        # ranged hücum: 1 ox atır, uzaqdan zərbə əlavə zərər verir
        if not self or not target:
            return 0
        if self.arrows > 0:
            self.arrows -= 1
            damage = self.attack_power + 10
        else:
            damage = self.attack_power // 2     # ox bitib, bıçaqla vurur
        return target.take_damage(damage)

    def get_info(self):
        return f"{super().get_info()}\nArrows: {self.arrows}"

    def get_special(self):
        return self.arrows


class Team:
    # Character + Character nəticəsində yaranan sadə komanda
    def __init__(self, members):
        self.members = members

    def __add__(self, other):
        # team + character -> yeni team
        return Team(self.members + [other])

    def __len__(self):
        return len(self.members)

    def __str__(self):
        names = ", ".join(member.name for member in self.members)
        return (f"Team: {names}\n"
                f"Members: {len(self)}\n"
                f"Total Health: {self.get_total_health()}\n"
                f"Total Attack Power: {self.get_total_attack_power()}")

    def get_total_health(self):
        return sum(member.health for member in self.members)

    def get_total_attack_power(self):
        return sum(member.attack_power for member in self.members)


# DB-dəki character_type dəyərinə görə hansı class istifadə olunacaq
CHARACTER_CLASSES = {
    'warrior': Warrior,
    'mage': Mage,
    'archer': Archer,
}
