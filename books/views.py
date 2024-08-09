from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from books.forms import ReviewForm
# Create your views here.


class DetailsBookView(DetailView) :
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'books/book_details.html'

    def post(self, request, *args, **kwargs) :
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid() :
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.name = f'{request.user.first_name} {request.user.last_name}'
            new_review.save()
            new_review = ''

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.review.all()
        review_form = ReviewForm()
        
        context['data'] = self.request.user
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context
