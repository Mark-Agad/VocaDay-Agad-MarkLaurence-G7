from django.conf import settings
from django.db import models


class Word(models.Model):
    word_text = models.CharField(max_length=50, unique=True)
    phonetic = models.CharField(max_length=100, blank=True)
    part_of_speech = models.CharField(max_length=50, blank=True)
    definition = models.TextField()
    example_sentence = models.TextField(blank=True)
    audio_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word_text


class SavedWord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_words',
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.PROTECT,
        related_name='saved_in',
    )
    date_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_saved']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'word'],
                name='unique_saved_word_per_user',
            ),
        ]

    def __str__(self):
        return f'{self.user} saved {self.word}'


class SearchLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='search_logs',
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.PROTECT,
        related_name='searched_in',
    )
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f'{self.user} searched {self.word}'