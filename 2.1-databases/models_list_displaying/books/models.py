# coding=utf-8

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Book(models.Model):
    name = models.CharField(u'Название', max_length=64)
    author = models.CharField(u'Автор', max_length=64)
    pub_date = models.DateField(u'Дата публикации')
    # slug = models.SlugField(max_length=64, db_index=True, null=True)

    def __str__(self):
        return self.name + " " + self.author

    # def get_absolute_url(self):
    #     return reverse('Book_detail', kwargs={'slug': self.slug})
    #
    # def save(self, *args, **kwargs):    # new
    #     if not self.slug:
    #         self.slug = slugify(self.pub_date)
    #     return super().save(*args, **kwargs)
