from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст не может быть менее 20 символов."
            })

        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичным названию."
            )

        return cleaned_data
