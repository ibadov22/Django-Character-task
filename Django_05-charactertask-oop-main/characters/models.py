from django.core.validators import MinValueValidator
from django.db import models

from .oop import CHARACTER_CLASSES


# Bu model yalnız məlumatı database-də saxlayır.
# Warrior / Mage / Archer Python class-larıdır (oop.py) - model inheritance YOXDUR.

class CharacterRecord(models.Model):
    CHARACTER_TYPES = [
        ('warrior', 'Warrior'),
        ('mage', 'Mage'),
        ('archer', 'Archer'),
    ]

    name = models.CharField(max_length=50)
    character_type = models.CharField(max_length=20, choices=CHARACTER_TYPES)
    health = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1)])
    attack_power = models.PositiveIntegerField(default=20, validators=[MinValueValidator(1)])
    # Warrior -> defense, Mage -> mana, Archer -> arrows
    special = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.get_character_type_display()}) - Health: {self.health}"

    def to_object(self):
        # database qeydi -> Python OOP obyekti (Warrior / Mage / Archer)
        character_class = CHARACTER_CLASSES[self.character_type]
        return character_class(self.name, self.health, self.attack_power, self.special)

    def update_from_object(self, character):
        # Python OOP obyekti -> database (hücumdan sonra yeni dəyərləri saxla)
        self.health = character.health
        self.special = character.get_special()
        self.save()
