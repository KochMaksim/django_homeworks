from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    # measurements

    # def __str__(self):
    #     return self.name


class Measurement(models.Model):
    temperature = models.FloatField(verbose_name="Температура С")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, related_name="measurements", verbose_name='Датчик')
    image = models.ImageField(upload_to='sensor/%Y/%m/%d/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
