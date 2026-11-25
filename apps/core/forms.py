from django import forms

from .models import CustomerReview


class ReviewSubmissionForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        label="",
        widget=forms.HiddenInput,
    )

    class Meta:
        model = CustomerReview
        fields = ("author_name", "rating", "text")
        labels = {
            "author_name": "Ваше имя",
            "rating": "Оценка",
            "text": "Ваш отзыв",
        }
        widgets = {
            "author_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "text": forms.Textarea(attrs={"rows": 5, "maxlength": 2000}),
        }

    def clean_author_name(self):
        return self.cleaned_data["author_name"].strip()

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if len(text) < 10:
            raise forms.ValidationError("Напишите отзыв не короче 10 символов.")
        if len(text) > 2000:
            raise forms.ValidationError("Отзыв не должен превышать 2000 символов.")
        return text

    def clean_website(self):
        website = self.cleaned_data["website"]
        if website:
            raise forms.ValidationError("Не удалось отправить отзыв.")
        return website
