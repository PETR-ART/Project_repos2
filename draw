import requests
import pygame
import sys
import os


def getmap(params=None):
    # proxy = {'http': 'http://proxy.volgotech.net:3128/', 'https': 'http://proxy.volgotech.net:3128/'}

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # response = requests.get(map_api_server, proxy=proxy, params=params)
    response = requests.get(map_api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_api_server)
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

    # Удаляем за собой файл с изображением.
    os.remove(file_name)

    # Преобразуем ответ в json-объект
    return response


