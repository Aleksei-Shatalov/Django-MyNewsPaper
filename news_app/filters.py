from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
from django.forms import DateInput


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
    )

    created_after = DateFilter(
        field_name='created_at',
        lookup_expr='gte',  # фильтрация "больше или равно"
        label='Создано после',
        widget=DateInput(attrs={'type': 'date'})  # добавляем виджет для календаря
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }