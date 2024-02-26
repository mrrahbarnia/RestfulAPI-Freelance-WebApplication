from django.test import TestCase

from skill.models import (
    Category,
    Skill
)
from ...services.skills import (
    create_category,
    create_skill
)


class TestSkillLogics(TestCase):

    def test_create_category(self):
        sample_category = create_category(name='IT')

        self.assertIn(sample_category, Category.objects.all())

    def test_create_skill(self):
        sample_category = create_category(name='IT')
        sample_skill = create_skill(name='Django', category=sample_category)

        self.assertIn(sample_skill, Skill.objects.all())
