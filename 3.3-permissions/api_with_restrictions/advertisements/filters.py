from django_filters import rest_framework as filters, CharFilter, DateFromToRangeFilter, DateTimeFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # переопределяются поле модели которые имеют сложную логику
    creator = CharFilter(field_name='creator', lookup_expr='id')

    # для фильтрации по дате и времени используем DateTimeFromToRangeFilter
    # created_at = DateFromToRangeFilter()
    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status']
