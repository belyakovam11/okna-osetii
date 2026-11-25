from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from apps.core.pricing import calculate_window_prices
from .forms import (
    LoginForm,
    OrderRequestForm,
    ProfileForm,
    REGION_SUGGESTIONS,
    RegistrationForm,
)
from .models import OrderRequest, UserProfile


def _safe_next_url(request):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def register(request):
    if request.user.is_authenticated:
        return redirect(_safe_next_url(request) or "user_profile")
    form = RegistrationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация прошла успешно.")
        return redirect(_safe_next_url(request) or "user_profile")
    return render(request, "users/account_form.html", {
        "form": form,
        "page_title": "Создать аккаунт",
        "submit_label": "Зарегистрироваться",
        "alternate_url": "user_login",
        "alternate_label": "Уже есть аккаунт? Войти",
        "next": _safe_next_url(request),
        "is_registration": True,
        "regions": REGION_SUGGESTIONS,
    })


def user_login(request):
    if request.user.is_authenticated:
        return redirect(_safe_next_url(request) or "user_profile")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(_safe_next_url(request) or "user_profile")
    return render(request, "users/account_form.html", {
        "form": form,
        "page_title": "Войти в аккаунт",
        "submit_label": "Войти",
        "alternate_url": "user_register",
        "alternate_label": "Нет аккаунта? Зарегистрироваться",
        "next": _safe_next_url(request),
    })


@login_required
def user_logout(request):
    if request.method != "POST":
        return redirect("home")
    logout(request)
    return redirect("home")


@login_required
def user_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    is_order_submission = request.method == "POST" and request.POST.get("form_type") == "order"
    form = ProfileForm(
        request.POST if request.method == "POST" and not is_order_submission else None,
        request.FILES if request.method == "POST" and not is_order_submission else None,
        instance=request.user,
        profile=profile,
    )
    order_initial = {
        key: request.GET[key]
        for key in ("material", "width", "height", "quantity")
        if key in request.GET
    }
    order_form = OrderRequestForm(
        data=request.POST if is_order_submission else None,
        initial=order_initial,
        profile=profile,
    )
    orders = OrderRequest.objects.filter(user=request.user).select_related("material")

    if request.method == "POST":
        if is_order_submission and order_form.is_valid():
            data = order_form.cleaned_data
            material = data["material"]
            _, _, total_price = calculate_window_prices(
                material.price,
                data["width"],
                data["height"],
                data["quantity"],
            )
            order = OrderRequest.objects.create(
                user=request.user,
                material=material,
                width=data["width"],
                height=data["height"],
                quantity=data["quantity"],
                total_price=total_price,
                phone=data["phone"],
                address=data["address"],
                comment=data["comment"],
            )
            messages.success(
                request,
                f"Заявка №{order.pk} отправлена менеджеру на подтверждение.",
            )
            return redirect("user_profile")
        if not is_order_submission and form.is_valid():
            form.save()
            messages.success(request, "Профиль сохранён.")
            return redirect("user_profile")

    return render(request, "users/profile.html", {
        "form": form,
        "order_form": order_form,
        "orders": orders,
        "profile": profile,
        "regions": REGION_SUGGESTIONS,
    })
