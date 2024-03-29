from django.test import TestCase

from skill.models import (
    Category,
    Skill
)
from ...services.skills import (
    create_category,
    create_skill,
    publish_category,
    publish_skill
)
from ...selectors.skills import (
    get_published_categories,
    get_published_skills,
)

class TestSkillLogics(TestCase):

    def test_create_category(self):
        sample_category = create_category(name='IT')

        self.assertIn(sample_category, Category.objects.all())

    def test_create_skill(self):
        sample_category = create_category(name='IT')
        sample_skill = create_skill(name='Django', category=sample_category)

        self.assertIn(sample_skill, Skill.objects.all())
    
    def test_get_published_categories(self):
        cat1 = create_category(name='Backend Development')
        cat1.published = True
        cat1.save()
        cat2 = create_category(name='UI')
        cat2.published = True
        cat2.save()

        categories = get_published_categories(name=None)
        self.assertIn(cat1, categories)
        self.assertIn(cat2, categories)
        self.assertEqual(categories.count(), 2)

    def test_get_published_skills(self):
        cat = create_category(name='Backend Development')
        empty_cat = create_category(name='Frontend Development')
        skill1 = create_skill(name='Django', category=cat)
        skill1.published = True
        skill1.save()
        skill2 = create_skill(name='FastAPI', category=cat)
        skill2.published = True
        skill2.save()

        skills = get_published_skills(category=None)
        self.assertIn(skill1, skills)
        self.assertIn(skill2, skills)
        self.assertEqual(skills.count(), 2)

        skills = get_published_skills(category=cat)
        self.assertEqual(skills.count(), 2)

        skills = get_published_skills(category=empty_cat)
        self.assertEqual(skills.count(), 0)
    
    def test_publish_category(self):
        sample_category = create_category(name='Backend')
        self.assertFalse(sample_category.published)

        publish_category(slug=sample_category.slug)
        sample_category.refresh_from_db()
        self.assertTrue(sample_category.published)


    def test_publish_skill(self):
        sample_category = create_category(name='Backend')
        sample_skill = create_skill(category=sample_category, name='Django')
        self.assertFalse(sample_skill.published)

        publish_skill(slug=sample_skill.slug)
        sample_skill.refresh_from_db()
        self.assertTrue(sample_skill.published)
