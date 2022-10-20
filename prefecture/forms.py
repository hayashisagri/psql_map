from django import forms
from django.core.exceptions import ValidationError

from prefecture.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("prefecture", "title", "text", "rate", "image")

    def clean_review(self):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        if len(title) > 100:
            raise ValidationError('タイトルは100文字以下にしてください。')
        elif len(text) > 100:
            raise ValidationError('本文は100文字以下にしてください。')
        return title, text
