
from django.urls import path
from .views import DepositMoneyView, borrow_book, BookDepositReportView

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit'),
    path('deposit_report/', BookDepositReportView.as_view(), name='deposit_report'),
    path('borrow/<int:book_id>', borrow_book, name='borrow_book'),
]
