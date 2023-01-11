from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from advertisements.models import Advertisement, Favorites


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user_status_open = Advertisement.objects.filter(
            status__exact='OPEN',
            creator=self.context["request"].user).\
            count()

        print(f'У пользователя {self.context["request"].user}, открытых объявлений: {user_status_open}')

        # проверка на закрытие статуса и количества открытых объявлений
        if data['status'] == 'CLOSED':
            return data
        elif user_status_open > 9:
            raise ValidationError("Пользователь не может иметь больше 10 открытых объявлений")

        return data


class FavoritesSerializer(serializers.ModelSerializer):
    """Serializer для избранных объявлений."""

    # user_favorites = UserSerializer(read_only=True)
    # adv = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ['id', 'user_favorites', 'adv']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_favorites'] = instance.user_favorites.username
        representation['adv'] = {"id": instance.adv.id, "title": instance.adv.title, "status": instance.adv.status}
        return representation

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # фильтр избранного объявления из всех
        favorite_adv = Advertisement.objects.filter(id=data['adv'].id)
        # фильтр избраных объявлений пользователя, на наличие нового
        user_favorites_qs = Favorites.objects.filter(adv_id__exact=data['adv'].id)

        # id пользов. на доб. объяв. в избранное != id пользов. создавшего объявление
        if data['user_favorites'].id != favorite_adv[0].creator.id:
            # .exists() - True, eсли есть объявления
            if user_favorites_qs.exists():
                raise ValidationError('Объявление с таким id есть в Избранном')
            else:
                return data
        else:
            raise ValidationError('Свое объявление нельзя добавить в Избранное')
