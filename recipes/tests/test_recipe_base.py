from django.test import TestCase
from recipes.models import Recipe, Category
from django.contrib.auth.models import User

# Create your tests here.


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name='Category name'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='recipe title',
            description='recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='min',
            servings=5,
            servings_unit='portions',
            preparation_steps='recipe preparation steps',
            preparation_steps_is_html=False,
            is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

