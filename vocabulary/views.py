from django.contrib import messages
from django.shortcuts import render

from accounts.decorators import role_required
from accounts.models import User
from .forms import SearchForm
from .services import lookup_word, WordNotFound, DictionaryUnavailable


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
            messages.error(request, 'Please enter a valid word.')

    return render(request, 'vocabulary/search.html', {'form': form, 'result': result})