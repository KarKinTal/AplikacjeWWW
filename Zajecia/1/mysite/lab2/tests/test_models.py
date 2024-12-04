from django.test import TestCase
from ..models import Person, Team

class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.create(name='Jan', shirt_size='L')

    def test_first_name_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_first_name_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field('name').max_length
        self.assertEqual(max_length, 60)

class TeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Team.objects.create(name='Winners', country='US')

    def test_team_name_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_team_country_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('country').verbose_name
        self.assertEqual(field_label, 'country')

class AdditionalPersonModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person1 = Person.objects.create(name='Anna', shirt_size='M')
        cls.person2 = Person.objects.create(name='Tom', shirt_size='S')

    def test_unique_ids(self):
        self.assertNotEqual(self.person1.id, self.person2.id)