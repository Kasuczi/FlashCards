from django.db import models
from django.conf import settings


class FlashcardsModel(models.Model):
    CATEGORIES = [
        ('Python', 'Python'),
        ('GitHub', 'GitHub')
    ]
    flashcard_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40)
    text_content = models.TextField(max_length=255)
    answer = models.CharField(max_length=100, blank=True)
    user_answer_1 = models.CharField(max_length=50, blank=True)
    user_answer_2 = models.CharField(max_length=50, blank=True)
    user_answer_3 = models.CharField(max_length=50, blank=True)
    user_answer_4 = models.CharField(max_length=50, blank=True)
    right_answer = models.CharField(max_length=50, blank=True)
    flashcard_source = models.CharField(max_length=100, blank=True)
    flashcard_category = models.CharField(choices=CATEGORIES,
                                          max_length=50)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='flashcards_liked',
                                        blank=True)
