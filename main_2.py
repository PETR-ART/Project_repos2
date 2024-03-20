import requests
import pygame
import sys
import os


toponym_to_find = 'Россия'


def geocode(toponym_to_find):
    proxy = {'http': 'http://proxy.volgatech.net:3128/', 'https': 'http://proxy.volgatech.net:3128/'}
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, proxies=proxy, params=geocoder_params)
    # response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print("Ошибка выполнения запроса ", response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

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
    upper = list(map(float, toponym["boundedBy"]['Envelope']['upperCorner'].split()))
    # Долгота и широта:
    return [str(abs(lower[0] - upper[0]) / 2), str(abs(lower[1] - upper[1]) / 2)]


def get_map(params=None):
    proxy = {'http': 'http://proxy.volgatech.net:3128/', 'https': 'http://proxy.volgatech.net:3128/'}

    map_api_server = "http://static-maps.yandex.ru/1.x/"

    response = requests.get(map_api_server, proxies=proxy, params=params)
    # response = requests.get(map_api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса ", response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # инициализация игры
    pygame.init()
    window = pygame.display.set_mode(600, 450)

    file_name = "map.png"
    with open(file_name, "wb") as file:
        file.write(response.content)

    window.blit(pygame.image.load(file_name), (0, 0))
    pygame.display.flip()

    # Переменные, определяющие текущий масштаб карты и изменение масштаба
    current_scale = float(spn[0])
    scale_step = 0.1

    # Обработка событий клавиш PgUp и PgDown
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                current_scale += scale_step
            elif event.key == pygame.K_PAGEDOWN:
                current_scale -= scale_step

        # Проверяем, что масштаб не выходит за пределы
        current_scale = max(0.01, min(10, current_scale))
        spn[0] = str(current_scale)

        # Собираем параметры для запроса к Static Maps API:
        map_params = {"ll": ",".join(coord), "spn": ",".join(spn), "l": "map"}

        response = get_map(map_params)
        
        pygame.display.flip()

    # Удаляем за собой файл с изображением.
    os.remove(file_name)

    # Преобразуем ответ в json-объект
    return response


if __name__ == '__main__':
    response = geocode(toponym_to_find)
    if response:
        coord = get_coord(response)
        spn = get_spn(response)

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join(coord),
            "spn": ",".join(spn),
            "l": "map"
        }

        response = get_map(map_params)
