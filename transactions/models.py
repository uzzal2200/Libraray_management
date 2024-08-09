
from django.db import models
from accounts.models import UserAccount
from books.models import Book

class DepositUser(models.Model):
    account = models.ForeignKey(UserAccount, related_name = 'deposit', on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']

    def __str__(self) :
        return self.account.account_number

class BorrowBook(models.Model):
    account = models.ForeignKey(UserAccount, related_name = 'borrow', on_delete = models.CASCADE)
    book = models.ForeignKey(Book, related_name = 'borrow', on_delete = models.CASCADE)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    return_book = models.BooleanField(default=False)

    class Meta:
        ordering = ['borrowed_time']

    def __str__(self) :
        return str(self.account.account_number)
