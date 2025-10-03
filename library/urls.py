
from django.urls import path
from . import views
from .views import BookListView, BookDetailView, BookCreateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', views.book_list, name='book_list'),  # Home page shows books
    path('', BookListView.as_view(), name='book_list'),
    # path('book/<int:pk>', BookDetailView.as_view(), name="book_detail"),
    path('book/<slug:slug>', BookDetailView.as_view(), name="book_detail"),
    path('about/', views.about, name='about'),    # About page
    path('books/add/', views.BookCreateView.as_view(), name='book_add'),  # Add book page
    path('book/<slug:slug>/edit/', views.BookUpdateView.as_view(), name='book_edit'),  # Edit book page
    path('book/<slug:slug>/delete/', views.BookDeleteView.as_view(), name='book_delete'),  # Delete book page
    
    # function based views
    path('book/<slug:slug>/review/', views.add_review, name='add_review'),  # Add review to a book
    path('book/<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),  # Favorite or unfavorite a book
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)