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
    # assert True, "Just test example"

    # Arrange, подготовка данных, чт./зп. БД
    course = course_factory(_quantity=5)
    url = reverse("courses-list")

    # Act, тестируемый функционал
    response = client.get(url)

    # Assert, проверка корректности действий
    assert response.status_code == 200
    resp_json = response.json()
    # проверка списка курсов
    assert len(resp_json) == len(course)
    for i, crs in enumerate(resp_json):
        # проверка возврата запрошенного курса
        assert crs['id'] == course[i].id
        # проверка имен всех курсов
        assert crs['name'] == course[i].name


@pytest.mark.django_db
def test_course_filter_id(client, course_factory):
    url = reverse("courses-list")
    course = course_factory(_quantity=4)

    response = client.get(url)

    assert response.status_code == 200
    resp_json = response.json()
    for crs in resp_json:
        course_id = Course.objects.filter(id__exact=crs['id'])
        oourse_name = Course.objects.filter(name__exact=crs['name'])
        # проверка результата запроса с фильтром по id
        assert crs['id'] == course_id[0].id
        # проверка результата запроса с фильтром по name
        assert crs['name'] == oourse_name[0].name

@pytest.mark.django_db
def test_course_create(client):
    url = reverse("courses-list")
    course_json = {"name": "New"}

    resp_post = client.post(url, course_json)

    # тест успешного создания курса
    assert resp_post.status_code == 201
    resp_post_json = resp_post.json()
    assert resp_post_json["name"] == 'New'


@pytest.mark.django_db
def test_course_patch(client, course_factory):
    course_fct = course_factory(_quantity=4)
    url_detail = reverse("courses-detail", args=[course_fct[2].id])    # непонятно, можно ли взять id всех записей ???
    url_list = reverse("courses-list")
    course_json = {"name": "A"}

    resp_patch = client.patch(url_detail, course_json)
    # response = client.patch(f'/api/v1/courses?id={course.id}', data={"name": "new", "students": "new_st"})
    resp_get = client.get(url_list)

    assert resp_patch.status_code == 200  # or 301
    # assert resp_patch.status_code == 301
    resp_get_json = resp_get.json()
    assert len(resp_get_json) == len(course_fct)
    resp_patch_json = resp_patch.json()
    assert resp_patch_json['name'] == "A"
    # проверка всех объектов, что в одном было изминение в поле 'name'
    for r in resp_get_json:
        if r['name'] == course_json["name"]:
            assert True
            break
    else:
        assert False, f'not {course_json}'


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    course_fct = course_factory(_quantity=4)
    url_detail = reverse("courses-detail", args=[course_fct[2].id])
    url_list = reverse("courses-list")

    resp_del = client.delete(url_detail)
    resp_get = client.get(url_list)

    assert resp_del.status_code == 204
    resp_get_json = resp_get.json()
    assert len(resp_get_json) == len(course_fct) - 1
