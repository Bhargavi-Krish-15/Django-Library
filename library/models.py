from django.db import models
# reverse is used to get the URL for a specific view by its name
from django.urls import reverse
# slugify is used to create URL-friendly slugs from strings
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
# Author, Genre, Publisher, Book Models
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # meta is used to define model-level options, like ordering , verbose_name, etc.
    # this is used to specify the default ordering of Author objects when they are retrieved from the database.
    class Meta:
        ordering = ['last_name', 'first_name']

    # string representation of the object, which is useful for displaying the object in the Django admin interface and other places.
    def __str__(self):
        return f" {self.first_name} {self.last_name} "


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    # author = models.CharField(max_length=100)
    publish_date = models.DateField()

    subtitle = models.CharField(max_length=100, blank=True)
    # many to many because a book can have multiple authors and an author can write multiple books
    authors = models.ManyToManyField(Author, verbose_name=("Author"))
    # foreign key because a book can have only one publisher but a publisher can publish multiple books
    publisher = models.ForeignKey(
        Publisher, null=True, blank=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField(Genre, verbose_name=("Genre"))
    summary = models.TextField(blank=True)
    # image field for book cover
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)

    # slug is for better url simply to look nice
    # initially dont give unique=True , which doesnt work and throws error while creating migrations
    # later after creatign teh model, change it to unique=True and create a new migration
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)

    # automatically sets the field to the current date and time every time the object is saved
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date', 'title']

    def __str__(self):
        # return f" {self.title} - {self.authors} "
        authors = ", ".join(str(a) for a in self.authors.all())
        return f"{self.title} - {authors}"

    def get_absolute_url(self):
        # this is used to get the URL for the detail view of a Book object
        # kwargs is used to pass the slug of the book to the URL pattern
        return reverse("book_detail", kwargs={"slug": self.slug})

    # This method is called when the object is saved to the database. It generates a unique slug from the book title if the slug is not already set.
    def save(self, *args, **kwargs):
        
        """
        if slug is not set, generate it from the title
        slugify is used to create a URL-friendly slug from the book title
        check if the slug already exists in the database, and if it does, append a counter to make it unique
        finally, call the parent class's save method to save the object to the database
        this ensures that every book has a unique slug based on its title
        this is important for creating SEO-friendly URLs and avoiding conflicts in the URL namespace
        the while loop checks if a book with the same slug already exists in the database, and if it does, it appends a counter to the slug until a unique slug is found
        slugify is used to create a URL-friendly slug from the book title
        super() is used to call the parent class's save method to save the object to the database
        """
        
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ["-created_at"]
        # to review book only once by a particular user
        unique_together = ('book','user')
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"

class Favorite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_by")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ["-created_at"]
        # to favorite book only once by a particular user
        unique_together = ('book','user')
    
    def __str__(self):
        return f"{self.user.username} ❤️ {self.book.title}"
