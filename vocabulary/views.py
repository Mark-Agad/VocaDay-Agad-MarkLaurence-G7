from urllib.parse import quote

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from accounts.models import User
from .forms import SearchForm
from .models import Word, SavedWord, SearchLog
from .services import lookup_word, WordNotFound, DictionaryUnavailable


def store_word(word, result):
    """Save the word once in the Word table (BR-11)."""
    first_meaning = result['meanings'][0] if result['meanings'] else {}
    definitions = first_meaning.get('definitions', [])
    first_def = definitions[0] if definitions else {}

    word_obj, created = Word.objects.get_or_create(
        word_text=word,
        defaults={
            'phonetic': result['phonetic'],
            'part_of_speech': first_meaning.get('part_of_speech', ''),
            'definition': first_def.get('definition', ''),
            'example_sentence': first_def.get('example', ''),
            'audio_url': result['audio'],
        },
    )
    return word_obj


@role_required(User.MEMBER)
def search_view(request):
    form = SearchForm(request.GET or None)
    result = None
    searched_word = None
    is_saved = False

    if form.is_bound:
        if form.is_valid():
            word = form.cleaned_data['word']
            try:
                result = lookup_word(word)
            except WordNotFound:
                messages.error(request, f'No definition found for "{word}".')
            except DictionaryUnavailable:
                messages.error(
                    request,
                    'The dictionary service is unreachable right now. Please try again later.',
                )
            else:
                word_obj = store_word(word, result)
                # Coming back after a save is not a new search, so don't log it again
                if not request.GET.get('saved'):
                    SearchLog.objects.create(user=request.user, word=word_obj)
                searched_word = word
                is_saved = SavedWord.objects.filter(
                    user=request.user, word=word_obj
                ).exists()
        else:
            messages.error(request, 'Please enter a valid word.')

    return render(request, 'vocabulary/search.html', {
        'form': form,
        'result': result,
        'searched_word': searched_word,
        'is_saved': is_saved,
    })


@role_required(User.MEMBER)
@require_POST
def save_word_view(request):
    word_text = request.POST.get('word', '').strip().lower()

    try:
        word_obj = Word.objects.get(word_text=word_text)
    except Word.DoesNotExist:
        messages.error(request, 'Search for the word first before saving it.')
        return redirect('vocabulary:search')

    saved, created = SavedWord.objects.get_or_create(
        user=request.user, word=word_obj
    )
    if created:
        messages.success(request, f'"{word_text}" was saved to your list.')
    else:
        messages.error(request, f'"{word_text}" is already in your saved words.')

    return redirect(f"{reverse('vocabulary:search')}?word={quote(word_text)}&saved=1")