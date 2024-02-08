from io import BytesIO
from PIL import Image

import sys
import aa
import draw

toponym_to_find = " ".join(sys.argv[1:])

if __name__ == '__main__':
    response = aa.geocode(toponym_to_find)
    if response:
        coord = aa.get_coord(response)
        spn = aa.get_spn(response)

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join(coord),
            "spn": ",".join(spn),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = draw.get_map(map_params)

        Image.open(BytesIO(response.content)).show()
        # Создадим картинку
        # и тут же ее покажем встроенным просмотрщиком операционной системы
