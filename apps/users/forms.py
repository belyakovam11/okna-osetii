from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from apps.gallery.models import Materials
from .models import UserProfile


REGION_SUGGESTIONS = (
    "Республика Северная Осетия — Алания",
    "Республика Ингушетия",
    "Кабардино-Балкарская Республика",
    "Чеченская Республика",
    "Республика Дагестан",
    "Карачаево-Черкесская Республика",
    "Ставропольский край",
)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Электронная почта", required=False)
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    region = forms.CharField(
        label="Регион",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "list": "region-options",
                "placeholder": "Выберите или укажите регион",
            }
        ),
    )
    address = forms.CharField(label="Адрес", required=False, max_length=255)
    phone = forms.CharField(label="Телефон", required=False, max_length=20)
    avatar = forms.ImageField(label="Аватар", required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        labels = {"username": "Логин"}

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Размер изображения не должен превышать 5 МБ.")
        return avatar

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.create(
                user=user,
                avatar=self.cleaned_data.get("avatar"),
                region=self.cleaned_data.get("region", ""),
                address=self.cleaned_data.get("address", ""),
                phone=self.cleaned_data.get("phone", ""),
            )
        return user


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label="Электронная почта", required=False)
    phone = forms.CharField(label="Телефон", required=False, max_length=20)
    region = forms.CharField(
        label="Регион",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "list": "region-options",
                "placeholder": "Выберите или укажите регион",
            }
        ),
    )
    address = forms.CharField(label="Адрес", required=False, max_length=255)
    avatar = forms.ImageField(label="Аватар", required=False)

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, profile, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)
        self.fields["region"].initial = profile.region
        self.fields["address"].initial = profile.address
        self.fields["phone"].initial = profile.phone

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Размер изображения не должен превышать 5 МБ.")
        return avatar

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            self.profile.region = self.cleaned_data["region"]
            self.profile.address = self.cleaned_data["address"]
            self.profile.phone = self.cleaned_data["phone"]
            avatar = self.cleaned_data.get("avatar")
            if avatar:
                self.profile.avatar = avatar
            self.profile.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class OrderRequestForm(forms.Form):
    material = forms.ModelChoiceField(
        queryset=Materials.objects.all(),
        label="Материал",
    )
    width = forms.IntegerField(
        label="Ширина, мм",
        min_value=100,
        max_value=6000,
    )
    height = forms.IntegerField(
        label="Высота, мм",
        min_value=100,
        max_value=6000,
    )
    quantity = forms.IntegerField(
        label="Количество окон",
        min_value=1,
        max_value=50,
    )
    phone = forms.CharField(label="Телефон", max_length=20)
    address = forms.CharField(label="Адрес", max_length=255)
    comment = forms.CharField(
        label="Комментарий к заказу",
        required=False,
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    def __init__(self, *args, profile, **kwargs):
        initial = kwargs.setdefault("initial", {})
        initial.setdefault("phone", profile.phone)
        initial.setdefault("address", profile.address)
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if len(phone) < 7:
            raise forms.ValidationError("Укажите телефон для связи.")
        return phone

    def clean_address(self):
        return self.cleaned_data["address"].strip()

    def clean_comment(self):
        return self.cleaned_data["comment"].strip()

    def clean_material(self):
        material = self.cleaned_data["material"]
        if material.price <= 0:
            raise forms.ValidationError(
                "Для выбранного материала не задана цена за м²."
            )
        return material
