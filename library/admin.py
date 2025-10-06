from django.contrib import admin
from .models import Book, Author, Genre, Publisher, Review, Favorite

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # list_display is used to specify the fields to be displayed in the admin list view in a tabular format.
    # search_fields is used to specify the fields that can be searched using the search box in the admin interface.
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ('name',)
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','publisher', 'publish_date')
    # list filter is used to specify the fields that can be used to filter the list of objects in the admin interface.
    list_filter = ('publisher', 'genres', 'publish_date')   # plural genres
    search_fields = ('title', 'authors__first_name', 'authors__last_name')
    # prepopulated_fields = {'slug': ('title',)}
    # filter_horizontal is used to display a horizontal filter widget for many-to-many relationships in the admin interface.
    # filter_horizontal = ('genres',)              

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','book', 'rating', 'comment')
    search_fields = ('book',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('book','user',)    
    search_fields = ('book',)
    
