import requests


def geocode(toponym_to_find):
    # proxy = {'http': 'http://proxy.volgotech.net:3128/', 'https': 'http://proxy.volgotech.net:3128/'}

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    # response = requests.get(geocoder_api_server, proxy=proxy, params=geocoder_params)
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        return

    # Преобразуем ответ в json-объект
    return response.json()


def get_coord(json_response):
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    return toponym_coodrinates.split(" ")


def get_spn(json_response):
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    lower = list(map(float, toponym["boundedBy"]['Envelope']['lowerCorner'].split()))
    upper = list(map(float, ["boundedBy"]['Envelope']['upperCorner'].split()))
    # Долгота и широта:
    return [str(abs(lower[0] - upper[0]) / 2), str(abs(lower[1] - upper[1]) / 2)]
