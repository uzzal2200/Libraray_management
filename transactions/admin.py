from django.contrib import admin
from .models import DepositUser, BorrowBook

# Register your models here.

admin.site.register(DepositUser)
admin.site.register(BorrowBook)