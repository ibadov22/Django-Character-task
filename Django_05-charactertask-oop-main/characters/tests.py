from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from characters.models import CharacterRecord
from characters.oop import Character, Warrior, Mage, Archer, Team


class OopTests(SimpleTestCase):
    def setUp(self):
        self.warrior = Warrior("Ali", 100, 20, 5)
        self.mage = Mage("Vali", 70, 25, 30)
        self.archer = Archer("Aysel", 80, 15, 5)

    def test_create(self):
        character = Character("Base", 80, 10)
        self.assertEqual(character.name, "Base")
        self.assertEqual(character.health, 80)
        self.assertEqual(character.attack_power, 10)

    def test_inheritance(self):
        for character in (self.warrior, self.mage, self.archer):
            self.assertIsInstance(character, Character)

    def test_polymorphism(self):
        dummy = Character("Dummy", 500, 0)
        damages = [c.attack(dummy) for c in (self.warrior, self.mage, self.archer)]
        self.assertEqual(damages, [25, 50, 25])
        self.assertEqual(dummy.health, 400)

    def test_str(self):
        self.assertEqual(str(Character("Ali", 100, 20)),
                         "Character: Ali\nHealth: 100\nAttack Power: 20")

    def test_add(self):
        team = self.warrior + self.mage
        self.assertIsInstance(team, Team)
        self.assertEqual(len(team), 2)
        self.assertEqual(len(team + self.archer), 3)

    def test_lt_eq_len(self):
        self.assertTrue(self.warrior < self.mage)
        self.assertFalse(self.mage < self.warrior)
        self.assertFalse(self.warrior == self.mage)
        self.assertTrue(self.warrior == Warrior("Ali", 100, 20, 5))
        self.assertEqual(len(self.warrior), 100)

    def test_damage_and_bool(self):
        victim = Character("Victim", 30, 5)
        self.assertTrue(victim)
        self.assertEqual(self.warrior.attack(victim), 25)
        self.assertEqual(victim.health, 5)
        self.assertEqual(self.mage.attack(victim), 5)
        self.assertEqual(victim.health, 0)
        self.assertFalse(victim)

    def test_dead_cannot_attack(self):
        dead = Character("Dead", 0, 10)
        self.assertEqual(dead.attack(self.warrior), 0)
        self.assertEqual(self.warrior.attack(dead), 0)

    def test_warrior_defense(self):
        self.assertEqual(self.warrior.take_damage(8), 3)


class DjangoTests(TestCase):
    def setUp(self):
        self.warrior = CharacterRecord.objects.create(
            name="Ali", character_type="warrior", health=100, attack_power=20, special=5)
        self.mage = CharacterRecord.objects.create(
            name="Vali", character_type="mage", health=70, attack_power=25, special=30)

    def test_pages_open(self):
        for name in ('home', 'characters:characters_list', 'characters:character_create',
                     'characters:character_attack', 'characters:oop_demo'):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)

    def test_create_character(self):
        response = self.client.post(reverse('characters:character_create'), {
            'name': 'Aysel', 'character_type': 'archer',
            'health': 80, 'attack_power': 15, 'special': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CharacterRecord.objects.count(), 3)

    def test_attack(self):
        self.client.post(reverse('characters:character_attack'), {
            'attacker': self.warrior.pk, 'target': self.mage.pk,
        })
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.health, 45)      # 70 - (20 + 5)

    def test_cannot_attack_self(self):
        self.client.post(reverse('characters:character_attack'), {
            'attacker': self.warrior.pk, 'target': self.warrior.pk,
        })
        self.warrior.refresh_from_db()
        self.assertEqual(self.warrior.health, 100)
