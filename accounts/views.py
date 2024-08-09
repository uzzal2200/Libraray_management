
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from transactions.models import BorrowBook
from django.views.generic import ListView
from django.contrib import messages

class UserRegistrationView(FormView) :
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form) :
        user = form.save()
        return super().form_valid(form)


class UserAccountUpdateView(LoginRequiredMixin, View):
    template_name = 'accounts/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class UserLoginView(LoginView) :
    template_name = 'accounts/user_login.html'

    def get_success_url(self) :
        return reverse_lazy('home')


class UserLogoutView(LoginRequiredMixin, LogoutView) :
    def get_success_url(self) :
        if self.request.user.is_authenticated :
            logout(self.request)
        return reverse_lazy('home')


class BookBorrowReportView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    model = BorrowBook
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borroBook = BorrowBook.objects.filter(account=self.request.user.account)
        context['borroBook'] = borroBook
        return context
    
class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, borrow_id):
        book = get_object_or_404(BorrowBook, id=borrow_id)
        if not book.return_book:
            book.return_book = True
            user_account = book.account
            user_book = book.book
            user_account.balance += user_book.borrowing_price
            user_account.save()
            book.save()
            messages.success(
                request,
                f'Your are Returning a Book ({user_book.title}) successfully'
            )
        return redirect('profile')
