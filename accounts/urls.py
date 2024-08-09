
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserAccountUpdateView, BookBorrowReportView, ReturnBookView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', BookBorrowReportView.as_view(), name='profile'),
    path('profile/update/', UserAccountUpdateView.as_view(), name='Update_profile'),
    path('return_book/<int:borrow_id>',ReturnBookView.as_view(), name='return_book')
]
