import re

from django import forms


class SearchForm(forms.Form):
    word = forms.CharField(
        max_length=50,
        label='Word',
        widget=forms.TextInput(attrs={'placeholder': 'Type an English word'}),
    )

    def clean_word(self):
        word = self.cleaned_data['word'].strip().lower()
        if not re.fullmatch(r"[a-z]+(?:['-][a-z]+)*", word):
            raise forms.ValidationError(
                'Enter one English word (letters, hyphen or apostrophe only).'
            )
        return word