from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Book


def index(request):
    template = 'books/books_list.html'
    context = {}
    return render(request, template, context)


def books_view(request):
    template = 'books/books_view.html'
    books_objects = Book.objects.order_by('pub_date')
    context = {'books': books_objects}
    return render(request, template, context)


def show_book(request, pub_date):
    template = 'books/book.html'
    book_objects = Book.objects.filter(pub_date=pub_date)

    # Пред. книга по дате публикации. Отсортировать в БД, и достать первую пред. дату
    books_previous = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    books_next = Book.objects.filter(
        pub_date__gt=pub_date                                           # pub_date__gt - больше текущей даты pub_date
    ).order_by('pub_date').values_list('pub_date', flat=True).first()   # values_list + flat=True => list[]. first book

    context = {'page_obj': book_objects,
               'books_next': books_next,
               'books_previous': books_previous
               }
    return render(request, template, context)
