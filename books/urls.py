from django.urls import path
from .views import DetailsBookView

urlpatterns = [
    path('book_details/<int:id>', DetailsBookView.as_view(), name='book_details')
]