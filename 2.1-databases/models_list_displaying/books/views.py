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


def show_book(request, slug):
    template = 'books/book.html'
    book_objects = Book.objects.order_by('pub_date')
    page_start_num = 0
    slug_all = []
    for b in book_objects:
        slug_all.append(b.slug)        # save all pub_date in list

    for i in range(len(slug_all)):
        if slug_all[i] == slug:
            page_start_num = i+1              # start page number equals (index +1) list  slug_all
    print('slug_all:', slug_all)

    page_number = request.GET.get('page', page_start_num)
    print('page_number:', page_number)
    paginator = Paginator(book_objects, 1)
    page_obj = paginator.get_page(page_number)
    print('page_obj:', page_obj.object_list)

    # slug_prev = slug_all[int(page_number)-2]
    # slug_next = slug_all[int(page_number)]
    # print('slug_prev:', type(slug_prev), slug_prev)

    context = {'page_obj': page_obj,
               # 'slug_prev': slug_prev,
               # 'slug_next': slug_next
               }
    return render(request, template, context)
