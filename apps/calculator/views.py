from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Calculation
from .serializers import CalculationSerializer


class CalculationViewSet(viewsets.ModelViewSet):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer

    @action(detail=True, methods=['post'])
    def calculate_price(self, request, pk=None):
        """
        TODO: реализуйте расчёт стоимости окна.
        Подсказка: используйте поля profile, window_type, glass,
        width, height, quantity и сохраните результат в obj.price.
        """
        obj = self.get_object()
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Calculation
from .serializers import CalculationSerializer


# ─────────────────────────────────────────────────────────────
# Константы. ВАЖНО: всё в Decimal, а не в float!
# ─────────────────────────────────────────────────────────────
BASE_PRICE_PER_SQM = Decimal('5000.00')
MM_IN_METER = Decimal('1000')
TWO_PLACES = Decimal('0.01')

PROFILE_COEFFICIENTS = {
    'rehau': Decimal('1.20'),
    'kbe':   Decimal('1.10'),
    'veka':  Decimal('1.05'),
    'default': Decimal('1.00'),
}

WINDOW_TYPE_COEFFICIENTS = {
    'глухое':              Decimal('0.85'),
    'поворотное':          Decimal('1.00'),
    'поворотно-откидное':  Decimal('1.15'),
    'балконный блок':      Decimal('1.30'),
    'default':             Decimal('1.00'),
}

GLASS_COEFFICIENTS = {
    'однокамерный':        Decimal('0.90'),
    'двухкамерный':        Decimal('1.00'),
    'трёхкамерный':        Decimal('1.20'),
    'энергосберегающий':   Decimal('1.25'),
    'default':             Decimal('1.00'),
}


# ─────────────────────────────────────────────────────────────
# Хелперы — единственное место, где числа превращаются в Decimal
# ─────────────────────────────────────────────────────────────
def to_decimal(value, default='0'):
    """Безопасно приводит любое значение (int, float, str, None) к Decimal."""
    if value is None or value == '':
        return Decimal(default)
    try:
        # Если это float — сначала str(), чтобы избежать артефактов
        if isinstance(value, float):
            return Decimal(str(value))
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(default)


def round_money(value: Decimal) -> Decimal:
    """Округляет Decimal до копеек с обычным банковским округлением."""
    return value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def get_coefficient(mapping: dict, value) -> Decimal:
    """Возвращает коэффициент по названию или дефолтный."""
    if not value:
        return mapping['default']
    name = str(value).lower()
    for key, coeff in mapping.items():
        if key != 'default' and key in name:
            return coeff
    return mapping['default']


# ─────────────────────────────────────────────────────────────
# Основная функция расчёта — принимает простые типы (int/Decimal)
# ─────────────────────────────────────────────────────────────
def compute_price(profile_name, window_type_name, glass_name,
                  width, height, quantity) -> dict:
    """Возвращает словарь с ценой и коэффициентами. Никогда не падает."""
    width_d = to_decimal(width)
    height_d = to_decimal(height)
    quantity_d = to_decimal(quantity, default='1')

    if width_d <= 0 or height_d <= 0:
        raise ValueError('Ширина и высота должны быть больше нуля.')

    # мм → м²
    area_sqm = (width_d / MM_IN_METER) * (height_d / MM_IN_METER)

    profile_coeff = get_coefficient(PROFILE_COEFFICIENTS, profile_name)
    window_coeff = get_coefficient(WINDOW_TYPE_COEFFICIENTS, window_type_name)
    glass_coeff = get_coefficient(GLASS_COEFFICIENTS, glass_name)

    raw_price = (area_sqm
                 * BASE_PRICE_PER_SQM
                 * profile_coeff
                 * window_coeff
                 * glass_coeff
                 * quantity_d)

    return {
        'area_sqm': area_sqm.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
        'profile_coefficient': profile_coeff,
        'window_type_coefficient': window_coeff,
        'glass_coefficient': glass_coeff,
        'quantity': int(quantity_d),
        'price': round_money(raw_price),
    }
class CalculationViewSet(viewsets.ModelViewSet):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer

