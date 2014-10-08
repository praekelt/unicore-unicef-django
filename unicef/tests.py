import os
from django.test import TestCase
from django.core.management import call_command
from django.template.defaultfilters import slugify

from gitmodel.workspace import Workspace
from unicore_gitmodels import models

from post.models import Post
from category.models import Category


class ExportTest(TestCase):
    def create_categories(self, names=[u'Diarrhoea', u'Hygiene']):
        categories = []
        for name in names:
            category = Category(title=name)
            category.slug = slugify(name)
            category.save()
            categories.append(category)
        return categories

    def create_pages(self, count=2):
        pages = []
        for i in range(count):
            page = Post(
                title=u'Test Page %s' % (i,),
                content=u'this is sample content for pg %s' % (i,))
            page.save()
            pages.append(page)
        return pages

    def test_data_export(self):
        category1, category2 = self.create_categories()
        pages = self.create_pages(count=10)

        for page in pages[:8]:
            page.primary_category = category1
            page.save()

        for page in pages[8:]:
            page.primary_category = category2
            page.save()

        call_command('export_to_git', fake=True)

        repo_path = os.path.join(os.getcwd(), 'cms_temp_repo')
        ws = Workspace(repo_path)
        GitPage = ws.register_model(models.GitPageModel)
        GitCategory = ws.register_model(models.GitCategoryModel)

        self.assertEquals(len(list(GitCategory.all())), 2)
        self.assertEquals(len(list(GitPage.all())), 10)

        gitpage_1 = GitPage.filter(slug='test-page-1')[0]
        gitpage_2 = GitPage.filter(slug='test-page-9')[0]

        self.assertEquals(gitpage_1.primary_category.slug, 'diarrhoea')
        self.assertEquals(gitpage_1.language, 'eng_UK')
        self.assertEquals(gitpage_2.primary_category.slug, 'hygiene')
        self.assertEquals(gitpage_2.language, 'eng_UK')
