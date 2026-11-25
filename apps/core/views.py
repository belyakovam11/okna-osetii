from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render

from apps.core.pricing import calculate_window_prices
from apps.core.forms import ReviewSubmissionForm
from apps.core.models import CompletedWork, CustomerReview, HomePageAppearance
from apps.gallery.models import Materials


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "materials": Materials.objects.all(),
            "appearance": HomePageAppearance.objects.first(),
        },
    )


def reviews_and_works(request):
    review_form = ReviewSubmissionForm(request.POST or None)
    if request.method == "POST" and review_form.is_valid():
        review_form.save()
        messages.success(
            request,
            "Спасибо за отзыв! Он появится на сайте после проверки.",
        )
        return redirect("reviews_and_works")

    return render(
        request,
        "core/reviews_and_works.html",
        {
            "works": CompletedWork.objects.filter(is_published=True),
            "reviews": CustomerReview.objects.filter(is_published=True),
            "review_form": review_form,
        },
    )


def calculate_window_price(request):
    if request.method != "POST":
        return JsonResponse({"error": "Используйте POST-запрос."}, status=405)

    try:
        width = int(request.POST.get("width", ""))
        height = int(request.POST.get("height", ""))
        quantity = int(request.POST.get("quantity", "1"))
        material_id = int(request.POST.get("material", ""))
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Укажите материал, размеры и количество целыми числами."},
            status=400,
        )

    if not 100 <= width <= 6000 or not 100 <= height <= 6000:
        return JsonResponse(
            {"error": "Размеры окна должны быть от 100 до 6000 мм."},
            status=400,
        )
    if not 1 <= quantity <= 50:
        return JsonResponse(
            {"error": "Количество окон должно быть от 1 до 50."},
            status=400,
        )

    try:
        material = Materials.objects.get(pk=material_id)
    except Materials.DoesNotExist:
        return JsonResponse({"error": "Выберите материал из списка."}, status=400)

    try:
        price_per_sqm = Decimal(material.price)
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError(f"Некорректная цена материала {material.pk}.") from error
    if price_per_sqm <= 0:
        return JsonResponse(
            {"error": "Для выбранного материала не задана цена за м²."},
            status=400,
        )

    area, unit_price, total_price = calculate_window_prices(
        price_per_sqm,
        width,
        height,
        quantity,
    )
    return JsonResponse(
        {
            "material": material.name,
            "area": str(area.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)),
            "unit_price": str(unit_price),
            "quantity": quantity,
            "total_price": str(total_price),
            "currency": material.rub,
        }
    )
