import django_filters
from django.forms import CheckboxSelectMultiple

from .models import genre, toons_model,authors

class BookFilter(django_filters.FilterSet):
    genre = django_filters.ModelMultipleChoiceFilter(queryset=genre.objects.all(), widget=CheckboxSelectMultiple, label='Жанр')
    author = django_filters.ModelMultipleChoiceFilter(queryset=authors.objects.all(), widget=CheckboxSelectMultiple, label='Автор')
    class Meta:
        model = toons_model
        fields = ['genre', 'author']