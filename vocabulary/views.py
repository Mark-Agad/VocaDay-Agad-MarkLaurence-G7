from django.contrib import messages
from django.shortcuts import render

from accounts.decorators import role_required
from accounts.models import User
from .forms import SearchForm
from .models import Word, SearchLog
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
                SearchLog.objects.create(user=request.user, word=word_obj)
        else:
            messages.error(request, 'Please enter a valid word.')

    return render(request, 'vocabulary/search.html', {'form': form, 'result': result})