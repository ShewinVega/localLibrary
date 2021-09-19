from django.conf.urls import url
from django.urls import path
from django.views.generic.edit import DeleteView
from catalog.views import index, renew_book_librarian, BookListView, BookDetailView, AuthorListView, AuthorDetailView,LoanedBooksByUserListView, LoanedBooksForLibrarians, AuthorCreate, AuthorUpdate, AuthorDelete

catalog_patterns = ([
  path('', index, name='index'),
  path('books/',BookListView.as_view(), name='books'),
  path('book/<pk>',BookDetailView.as_view(), name='book-detail'),
  path('mybook/<pk>/renew/',renew_book_librarian, name='renew-book-librarian'),
  path('mybook/',LoanedBooksByUserListView.as_view(), name='my-borrowed'),
  path('myborrow/',LoanedBooksForLibrarians.as_view(), name='librarians'),
  path('authors/', AuthorListView.as_view(), name='authors'),
  path('author/<pk>', AuthorDetailView.as_view(), name='author-detail'),
  path('author/create/',AuthorCreate.as_view(), name='author_create'),
  path('author/<int:pk>/update', AuthorUpdate.as_view(), name='author_update'),
  path('author/<int:pk>/delete', DeleteView.as_view(), name='author_delete'),
],'catalog')