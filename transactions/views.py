from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from datetime import datetime
from django.db.models import Sum
from transactions.forms import DepositForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from transactions.models import DepositUser
from books.models import Book
from .models import BorrowBook
from django.urls import reverse
# Create your views here.


def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {'user': user, 'amount' : amount})
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class DepositMoneyView(LoginRequiredMixin, CreateView):
    form_class = DepositForm
    model = DepositUser
    template_name = 'transactions/deposit_form.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, 'Deposit Message', 'transactions/deposit_email.html')
        return super().form_valid(form)


def borrow_book(req, book_id):
    book = Book.objects.get(id=book_id)
    borrow_amount = book.borrowing_price
    if req.user.account.balance < borrow_amount:
        messages.error(
            req,
            f'{"{:,.2f}".format(float(borrow_amount))}$ is not enough to borrow this book'
        )
        return redirect('home')
    

    req.user.account.balance -= borrow_amount
    req.user.account.save(update_fields=['balance'])
    borrowbook = BorrowBook(account=req.user.account, book=book)
    borrowbook.save()
    messages.success(
            req,
            f'Your are Borrowing a Book ({book.title}) successfully'
        )
    send_transaction_email(req.user, borrow_amount, 'Book Borrowing Message', 'transactions/borrow_book_email.html')
    current_url = reverse('book_details', args=[book_id])
    return redirect(current_url)


class BookDepositReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/deposit_report.html'
    model = DepositUser
    balance = 0
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = DepositUser.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
