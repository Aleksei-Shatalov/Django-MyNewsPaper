from django import template

register = template.Library()

BAD_WORDS = ["редиска", "ругательство", "плохое"]


@register.filter(name='censor')
def censor(value):
    # Проверяем, что фильтр применяется к строке
    if not isinstance(value, str):
        raise ValueError("Censor filter can only be applied to strings.")

    for word in BAD_WORDS:
        # Цензурируем только целые слова, учитывая регистр первого символа
        value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
        value = value.replace(word.capitalize(), f"{word[0]}{'*' * (len(word) - 1)}")
    return value
