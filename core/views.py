from django.shortcuts import render
from books.models import Book
from category.models import Category

# Create your views here.

def index(req, category_slug = None) :
    data = Book.objects.all()
    if category_slug is not None :
        cate = Category.objects.get(slug=category_slug)
        data = Book.objects.filter(category=cate)
    
    category = Category.objects.all()
    return render(req, 'index.html', {'data' : data, 'category' : category})