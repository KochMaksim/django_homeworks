import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.fixture
def client():
    """Фикстура для клиента API."""
    return APIClient()


@pytest.fixture
def student_factory():
    """Фикстура для фабрики студентов."""
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    """Фикстура для фабрики курсов."""
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_course(client, course_factory):
    # Arrange, подготовка данных, чт./зп. БД
    courses = course_factory(_quantity=5)
    url = reverse("courses-list")

    # Act, тестируемый функционал
    response = client.get(url, HTTP_ACCEPT='application/json')
    # print(response.json())

    # Assert, проверка корректности действий
    assert response.status_code == 200
    resp_json = response.json()
    # проверка списка курсов
    assert len(resp_json) == len(courses)
    for i, crs in enumerate(resp_json):
        # проверка возврата запрошенного курса
        assert crs['id'] == courses[i].id
        # проверка имен всех курсов
        assert crs['name'] == courses[i].name


@pytest.mark.django_db
def test_course_detail(client, course_factory):
    courses = course_factory(_quantity=2)
    # course = courses[1]
    for course in courses:
        # print(f'course: {course}, {type(course)}, {course.id}')
        url_detail = reverse("courses-detail", args=[course.id])    # ex. "/api/v1/courses/7/"

        response = client.get(url_detail)
        # print(f'response: {response.json()}')

        assert response.status_code == 200
        resp_json = response.json()
        assert resp_json["id"] == course.id
        assert resp_json["name"] == course.name


@pytest.mark.django_db
def test_course_filter_id(client, course_factory):
    courses = course_factory(_quantity=4)
    url = reverse("courses-list")
    # задать номер курса для проверки деталей
    course = courses[1]

    # for course in courses:
    #     # print(f'course_name: {course.name}')
    #     response = client.get(url, {'id': course.id, 'name': course.name})

    response_1 = client.get(url, {"id": course.id})         # адрес "/api/v1/courses/?id=id_курса"
    response_2 = client.get(url, {"name": course.name})     # адрес "/api/v1/courses/?name=name_курса"
    print(f'response: {response_1.json()}')
    print(f'response: {response_2.json()}')

    assert response_1.status_code and response_2.status_code == 200
    # проверка результата запроса с фильтром по id и name
    assert response_1.json()[0]["id"] == course.id
    assert response_2.json()[0]["name"] == course.name

    # for crs in response.json():
    #     # фильтрация через БД
    #     course_id = Course.objects.filter(id__exact=crs['id'])
    #     course_name = Course.objects.filter(name__exact=crs['name'])


@pytest.mark.django_db
def test_course_create(client):
    url = reverse("courses-list")
    course_json = {"name": "New"}

    resp_post = client.post(url, course_json)

    # тест успешного создания курса
    assert resp_post.status_code == 201
    resp_post_json = resp_post.json()
    assert resp_post_json["name"] == course_json['name']


@pytest.mark.django_db
def test_course_patch(client, course_factory):
    courses_fct = course_factory(_quantity=4)
    url_detail = reverse("courses-detail", args=[courses_fct[2].id])
    url_list = reverse("courses-list")
    course_json = {"name": "ABC"}

    resp_patch = client.patch(url_detail, course_json)
    # response = client.patch(f'/api/v1/courses?id={course.id}', data={"name": "new", "students": "new_st"})

    # !!! get запрос сделал для себя !!! чтобы извлечь все объекты для проверки !!!
    resp_get = client.get(url_list)
    # print(f'resp_patch: {resp_patch.json()}')
    # print(f'resp_get: {resp_get.json()}')

    assert resp_patch.status_code == 200  # or 301
    resp_patch_json = resp_patch.json()
    assert resp_patch_json['name'] == course_json['name']

    # !!! Сделал для себя, чтобы проверить, что обновляется именно один выбранный объект !!!
    # проверка всех объектов, в одном было изминение в поле 'name', взятое из course_json
    resp_get_json = resp_get.json()
    for r in resp_get_json:
        if r['name'] == course_json["name"]:
            assert True, "Найден объект с искомым именем"
            break
    else:
        assert False, f'not {course_json}'


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses_fct = course_factory(_quantity=4)
    url_detail = reverse("courses-detail", args=[courses_fct[2].id])
    url_list = reverse("courses-list")

    resp_del = client.delete(url_detail)
    resp_get = client.get(url_list)

    assert resp_del.status_code == 204
    resp_get_json = resp_get.json()
    assert len(resp_get_json) == len(courses_fct) - 1
