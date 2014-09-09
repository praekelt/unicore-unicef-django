from category.models import Category
from django.shortcuts import render


def home(request):
    return render(
        request,
        'unicef/home.html',
        {'categories': Category.objects.all()})
