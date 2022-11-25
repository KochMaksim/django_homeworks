from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'kasha': {
        'молоко, л': 0.2,
        'овсяные хлопья, г': 50,
        'сливочное масло, г': 10,
        'соль, сахар, по вкусу!': 0,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }


def home_view(request):
    template_name = 'calculator/home.html'
    recipes_keys = DATA.keys()                          # All keys dictionary DATA
    context = {'recipes_all': recipes_keys}
    return render(request, template_name, context)


def recipes_view(request, recipe):
    template_name = 'calculator/index.html'
    num_serv = int(request.GET.get('servings', 1))      # Number of servings, default 1
    context = {'dish': recipe,                  # Adding a new key 'dish', servings with elements 'recipe', 'num_serv'
               'servings': num_serv
               }
    if recipe in DATA:
        context['recipe'] = {}                              # Adding a new key 'recipe' + creating a new nested dict.
        for ingredient, amount in DATA[recipe].items():
            context['recipe'][ingredient] = amount * num_serv   # Adding nested key "ingredient" + add. elem. "amount"
        return render(request, template_name, context)
    else:
        return render(request, template_name, context)

