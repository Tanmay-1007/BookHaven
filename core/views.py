# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Book, UserPreference, ReadingList, Review
from .forms import UserPreferenceForm, ReadingListForm, ReviewForm

def recommend_books(user):
    try:
        preferences = UserPreference.objects.get(user=user)
        favorite_genres = preferences.favorite_genres.split(',')
        favorite_authors = preferences.favorite_authors.split(',') if preferences.favorite_authors else []
        recommended = Book.objects.filter(
            Q(genre__in=favorite_genres) | Q(author__in=favorite_authors)
        ).distinct()
        return recommended
    except UserPreference.DoesNotExist:
        return Book.objects.none()

def home(request):
    search_query = request.GET.get('search', '')
    books = Book.objects.all()
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(genre__icontains=search_query)
        )
    recommended_books = recommend_books(request.user) if request.user.is_authenticated else Book.objects.none()
    return render(request, 'home.html', {
        'books': books,
        'recommended_books': recommended_books,
        'search_query': search_query,
    })

@login_required
def set_preferences(request):
    try:
        preferences = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        preferences = None

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preferences)
        if form.is_valid():
            preferences = form.save(commit=False)
            preferences.user = request.user
            preferences.save()
            messages.success(request, 'Preferences saved successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserPreferenceForm(instance=preferences)
    return render(request, 'set_preferences.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to BookHaven.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reading_list_entry = None
    user_review = None

    if request.user.is_authenticated:
        reading_list_entry = ReadingList.objects.filter(user=request.user, book=book).first()
        user_review = Review.objects.filter(user=request.user, book=book).first()

    if request.method == 'POST':
        if 'reading_list' in request.POST:
            reading_form = ReadingListForm(request.POST, instance=reading_list_entry)
            if reading_form.is_valid():
                reading_entry = reading_form.save(commit=False)
                reading_entry.user = request.user
                reading_entry.book = book
                reading_entry.save()
                messages.success(request, f'"{book.title}" updated in your reading list.')
                return redirect('book_detail', book_id=book.id)
            else:
                messages.error(request, 'Please select a valid status.')
        elif 'review' in request.POST:
            review_form = ReviewForm(request.POST, instance=user_review)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.book = book
                review.save()
                messages.success(request, 'Your review has been submitted!')
                return redirect('book_detail', book_id=book.id)
            else:
                messages.error(request, 'Please provide a valid rating.')
    else:
        reading_form = ReadingListForm(instance=reading_list_entry)
        review_form = ReviewForm(instance=user_review)

    reviews = Review.objects.filter(book=book).exclude(user=request.user)
    return render(request, 'book_detail.html', {
        'book': book,
        'reading_form': reading_form,
        'review_form': review_form,
        'reading_list_entry': reading_list_entry,
        'user_review': user_review,
        'reviews': reviews,
    })

@login_required
def reading_list(request):
    reading_list_entries = ReadingList.objects.filter(user=request.user)
    return render(request, 'reading_list.html', {'reading_list_entries': reading_list_entries})