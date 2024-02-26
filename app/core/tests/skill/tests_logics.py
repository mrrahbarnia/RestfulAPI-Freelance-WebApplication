from django.test import TestCase

from skill.models import (
    Category,
    Skill
)
from ...services.skills import (
    create_category,
    create_skill
)
from ...selectors.skills import (
    get_categories,
    get_skills
)

class TestSkillLogics(TestCase):

    def test_create_category(self):
        sample_category = create_category(name='IT')

        self.assertIn(sample_category, Category.objects.all())

    def test_create_skill(self):
        sample_category = create_category(name='IT')
        sample_skill = create_skill(name='Django', category=sample_category)

        self.assertIn(sample_skill, Skill.objects.all())
    
    def test_get_categories(self):
        cat1 = create_category(name='Backend Development')
        cat2 = create_category(name='UI')

        categories = get_categories()

        self.assertIn(cat1, categories)
        self.assertIn(cat2, categories)
        self.assertEqual(categories.count(), 2)

    def test_get_skills(self):
        cat = create_category(name='Backend Development')
        skill1 = create_skill(name='Django', category=cat)
        skill2 = create_skill(name='FastAPI', category=cat)

        skills = get_skills()

        self.assertIn(skill1, skills)
        self.assertIn(skill2, skills)
        self.assertEqual(skills.count(), 2)
