import os
import pygit2
import shutil

from django.core.management.base import BaseCommand

from optparse import make_option
from gitmodel.workspace import Workspace
from unicore_gitmodels import models

from post.models import Post
from category.models import Category

from html2text import html2text


class Command(BaseCommand):
    help = 'Save all the current content to a github repository'

    option_list = BaseCommand.option_list + (
        make_option(
            '--repo',
            action='store',
            dest='repo',
            default=False,
            help='The url for the github repository'),
        make_option(
            '--pubkey',
            action='store',
            dest='pubkey',
            default=False,
            help='The public key to use when pushing'),
        make_option(
            '--privkey',
            action='store',
            dest='privkey',
            default=False,
            help='The private key to use when pushing'),
        make_option(
            '--passphrase',
            action='store',
            dest='passphrase',
            default=None,
            help='The passphrase for the private key to use when pushing')
    )

    def push(self):
        for remote in self.repo.remotes:
            remote.credentials = self.credentials
            remote.push(self.repo.head.name)

    def delete_pages(self):
        for p in self.GitPage.all():
            self.GitPage.delete(
                p.uuid, True, message='Page deleted: %s' % p.title)

    def delete_categories(self):
        for c in self.GitCategory.all():
            self.GitCategory.delete(
                c.uuid, True,
                message='Category deleted: %s' % c.title)

    def save_post(self, instance):
        def update_fields(page, post):
            page.title = instance.title
            page.subtitle = instance.subtitle
            page.slug = instance.slug
            page.description = instance.description
            page.content = html2text(instance.content)
            page.created_at = instance.created
            page.modified_at = instance.modified
            page.featured_in_category = False
            page.featured = False
            page.language = 'eng_UK'

            if instance.primary_category:
                category = self.GitCategory.filter(
                    slug=instance.primary_category.slug)[0]
                page.primary_category = category

        page = self.GitPage()
        update_fields(page, instance)
        page.save(
            True, message='Page created: %s' % instance.title)

    def save_category(self, instance):
        def update_fields(category, post):
            category.title = instance.title
            category.subtitle = instance.subtitle
            category.slug = instance.slug
            category.language = 'eng_UK'
            category.featured_in_navbar = False

        category = self.GitCategory()
        update_fields(category, instance)
        category.save(
            True, message='Category created: %s' % instance.title)

    def handle(self, *args, **options):
        repo_url = options.get('repo')
        pubkey = options.get('pubkey')
        privkey = options.get('privkey')
        passphrase = options.get('passphrase')

        if not (repo_url or pubkey or privkey):
            raise Exception('Missing options. See usage.')

        print 'cloning repo..'

        repo_path = os.path.join(os.getcwd(), 'cmsrepo')

        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        self.credentials = pygit2.Keypair(
            'git',
            pubkey,
            privkey,
            passphrase)

        self.repo = pygit2.clone_repository(
            repo_url, repo_path, credentials=self.credentials)

        try:
            ws = Workspace(self.repo.path, self.repo.head.name)
        except pygit2.GitError:
            ws = Workspace(self.repo.path)

        self.GitPage = ws.register_model(models.GitPageModel)
        self.GitCategory = ws.register_model(models.GitCategoryModel)

        print 'deleting existing content..'
        self.delete_pages()
        self.delete_categories()

        print 'creating categories..'
        for c in Category.objects.all():
            self.save_category(c)

        print 'creating pages..'
        for p in Post.objects.all():
            self.save_post(p)

        print 'done.'

        print 'pushing to github..'
        self.push()
