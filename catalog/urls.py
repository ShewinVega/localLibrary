from django.conf.urls import url
from django.urls import path
from catalog.views import index, BookListView, BookDetailView

catalog_patterns = ([
  path('', index, name='index'),
  path('books/',BookListView.as_view(), name='books'),
  path('book/<pk>',BookDetailView.as_view(), name='book-detail')
],'catalog')