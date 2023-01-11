from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # заполняем связанные таблицы, с помощью списка positions
        for dan in positions:
            StockProduct.objects.create(
                stock=stock,
                product=dan['product'],
                quantity=dan['quantity'],
                price=dan['price']
            )
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # обновляем связанные таблицы или создаем product если такого нет
        for dan in positions:
            values_for_update = {'quantity': dan['quantity'], 'price': dan['price']}
            StockProduct.objects.update_or_create(
                stock=stock, product=dan['product'],    # критерий выборки объектов, которые будут обновляться
                defaults=values_for_update          # словарь пар(поле: значение), используемых для обновления объекта
            )
        return stock
