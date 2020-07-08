from django.contrib import admin
from .models import FlashcardsModel


# Register your models here.
@admin.register(FlashcardsModel)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('flashcard_id', 'title', 'text_content', 'answer')
    search_fields = ('title',)
