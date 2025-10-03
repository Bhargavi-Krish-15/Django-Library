from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# revers lazy is use so that the url is not loaded until all the urls configurations are loaded
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# function based views:
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Book, Review, Favorite
from .forms import ReviewForm

# Create your views here.
from .models import Book

# def book_list(request):
#     books = Book.objects.all()
#     return render(request, 'book_list.html', {'books': books})

def about(request):
    return render(request, 'about.html')

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    # object name is the name of the variable to use in the template to refer to the list of objects
    context_object_name = "books"
    # pagination to show 5 books per page in the book list view
    paginate_by = 5

class BookDetailView(DetailView):
    model = Book
    template_name =  'books/book_detail.html'
    context_object_name = "book"
    # to use slug instead of pk in the url
    # slug_field is the name of the field to use as the slug
    # slug_url_kwarg is the name of the URL keyword argument to use for the slug
    slug_field = "slug"
    slug_url_kwarg = "slug"
    
    # to pass additional context data to the template, like reviews and review form
    # we add a sperate method get_context_data to the BookDetailView class because the context data is dynamic and depends on the book being viewed
    # super() is used to call the parent class's get_context_data method to get the existing context data
    def get_context_data(self, **kwargs):
        # to prepare and supply the template with all the data (context variables) it needs to render properly.
        # if you want to add extra data to that default context—like your is_favorite flag or a review form—you override get_context_data.
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user = self.request.user
        # get all reviews for the book and setting that to the context dictionary 
        context['reviews'] = book.reviews.all()
        # to add a review form in the book detail view
        context['review_form'] = ReviewForm()
        
        # adding is_favorite to the context
        if user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(book=book, user=user).exists()
        else:
            context["is_favorite"] = False
        return context
 
# the add review is included as a function based view because it is a simple action that does not require a full class based view like CreateView
# also, it is easier to handle form submission and validation in a function based view
@login_required
def add_review(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        # here we bind the form to the POST data, so that we can validate and save it
        form = ReviewForm(request.POST)  
        if form.is_valid():
        #   review = form.save(commit=False)
        #   review.book = book
        #   review.user = request.user
        #   review.save()
        
            existing = Review.objects.filter(book=book, user=request.user).first()
            if existing:
                # Optionally: update the review, or show error message
                # existing.rating = form.cleaned_data['rating']
                # existing.comment = form.cleaned_data['comment']
                # existing.save()
                # messages.error(request, "You have already reviewed this book.")
                pass  # Replace or redirect as needed
            else:
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                
    # after saving the review, we redirect to the book detail view
    return redirect("book_detail", slug = slug)


@login_required
# this is used to either like or unlike a book
def toggle_favorite(request, slug):
    # get the book object based on the slug, or return a 404 error if not found
    book = get_object_or_404(Book, slug=slug)
    user = request.user
    # get the favorite object for the book and user, if it exists
    # if it exists, delete it (unfavorite), otherwise create it (favorite)
    favorite_qs = Favorite.objects.filter(book=book, user=user)
    if favorite_qs.exists():
        favorite_qs.delete()
    else:
        Favorite.objects.create(book=book, user=user)
    return redirect("book_detail", slug=slug)

    
# LoginRequiredMixin - to restrict access to authenticated users only, can be used only with class based views
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    # fields is a list of the model's fields to include in the form
    fields = ["title", "subtitle", "publish_date", "authors", "genres", "summary", "publisher"]
    template_name = "books/form/book_form.html"
    # success_url is the URL to redirect to after a successful form submission
    # here we use reverse_lazy to avoid circular imports which means the url is not loaded until all the urls configurations are loaded
    success_url = reverse_lazy("book_list")

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["title", "subtitle", "publish_date", "authors", "genres", "summary", "publisher"]
    template_name = "books/form/book_form.html"
    success_url = reverse_lazy("book_list")

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "books/form/book_confirm_delete.html"
    success_url = reverse_lazy("book_list")
    