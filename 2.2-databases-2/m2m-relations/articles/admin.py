from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import *


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_all = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            # print(f'form.cleaned_data: {form.cleaned_data}')
            if form.cleaned_data:
                is_main_all += (1 if form.cleaned_data['is_main'] else 0)
            else:
                break
            # print(f'form.cleaned_data[is_main]: {form.cleaned_data["is_main"]}')
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
            # raise ValidationError('Тут всегда ошибка')
        print(f'is_main_all: {is_main_all}')
        if is_main_all > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif is_main_all == 0:
            raise ValidationError('Укажите основной раздел')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInLine(admin.TabularInline):
    model = Article.tag_scope.through
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    inlines = [ScopeInLine]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    # inlines = [ScopeInLine]


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag', 'article', 'is_main']
