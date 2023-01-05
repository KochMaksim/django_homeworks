from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorites
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer, FavoritesSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AdvertisementFilter
    ordering_fields = ['id']

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [IsOwner()]
        elif self.action in ["destroy"]:
            return [IsOwner()]
        return []

    @action(methods=['get'], detail=False)
    def favorites(self, request):
        """Просмотр избранных объявлений"""

        # фильтр всех избранных объявлений пользователя
        user_favorites_qs = Favorites.objects.filter(user_favorites__exact=request.user)

        if len(user_favorites_qs) != 0:
            favorites_srl = FavoritesSerializer(user_favorites_qs, many=True)
            return Response(favorites_srl.data)
        raise ValidationError(f"У пользователя: {str(request.user)} - нет избранных объявлений")

    @action(methods=['post'], detail=False)
    def add_favorite(self, request):
        """Добавление объявлений в избранное"""

        # заполняем модель Favorites поле 'user_favorites' -> user_id пользователь добавивший объявление
        request.data['user_favorites'] = request.auth.user_id
        favorite_srl = FavoritesSerializer(data=request.data)
        favorite_srl.is_valid(raise_exception=True)
        favorite_srl.save()
        return Response(favorite_srl.data)
