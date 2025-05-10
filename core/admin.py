# core/admin.py
from django.contrib import admin
from .models import Book, UserPreference, ReadingList, Review

admin.site.register(Book)
admin.site.register(UserPreference)
admin.site.register(ReadingList)
admin.site.register(Review)