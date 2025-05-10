# core/forms.py
from django import forms
from .models import UserPreference, ReadingList, Review

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['favorite_genres', 'favorite_authors']
        widgets = {
            'favorite_genres': forms.TextInput(attrs={'placeholder': 'e.g., Fantasy,Science Fiction'}),
            'favorite_authors': forms.TextInput(attrs={'placeholder': 'e.g., J.R.R. Tolkien,Frank Herbert'}),
        }

class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('to_read', 'To Read'),
                ('reading', 'Reading'),
                ('read', 'Read'),
            ]),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'}),
        }