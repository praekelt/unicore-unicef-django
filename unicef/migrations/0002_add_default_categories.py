# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        #Add Other Site
        from category.models import Category

        if not Category.objects.filter(slug='hygiene').exists():
            category = Category.objects.create(title='Hygiene',
                                               slug='hygiene',
                                               )
            category.sites.add(1)
        if not Category.objects.filter(slug='diarrhoea').exists():
            category = Category.objects.create(title='Diarrhoea',
                                               slug='diarrhoea',
                                               )
            category.sites.add(1)

    def backwards(self, orm):
        from category.models import Category

        if Category.objects.filter(slug='hygiene').exists():
            Category.objects.get(slug='hygiene').delete()
        if Category.objects.filter(slug='diarrhoea').exists():
            Category.objects.get(slug='diarrhoea').delete()

    models = {
    }

    complete_apps = ['unicef']
    symmetrical = True
