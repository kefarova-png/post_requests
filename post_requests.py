import os
import time
import requests


class GoogleMapTest:
    def __init__(self):  # Создаем атрибуты экземпляра класса
        # Параметры тестируемого сайта:
        self.BASE_URL = "https://rahulshettyacademy.com"
        self.KEY_PARAM = {"key": "qaclick123"}  # для всех запросов
        self.POST_RESOUSE = "/maps/api/place/add/json"
        self.body = {
            "location": {"lat": -38.383494, "lng": 33.427362},
            "accuracy": 50,
            "name": "Frontline house",
            "phone_number": "(+91) 983 893 3937",
            "address": "29, side layout, cohen 09",
            "types": ["shoe park", "shop"],
            "website": "http://google.com",
            "language": "French-IN",
        }
        self.GET_RESOUSE = "/maps/api/place/get/json"
        # Переменная для имени файла, в который будем писать:
        self.FILE_NAME = "place_ids.txt"

    def post_get_5_times(self):
        print("\n-=Начало теста=-")

        try:
            # 1) Отправка 5-ти POST-запросов
            place_ids = []  # переменная для списка получаемых place_id
            post_url = f"{self.BASE_URL}{self.POST_RESOUSE}"  # путь для POST-запроса

            for i in range(5):
                print(f"Выполнение {i+1}-го (из 5-ти) POST-запроса")
                response = requests.post(post_url, params=self.KEY_PARAM, json=self.body)
                response_data = response.json()
                pid = response_data.get("place_id")  # place_id, полученный из ответа сервера
                place_ids.append(pid)  # добавляем каждый полученный place_id в файл

            # 2) Создание текстового файла и запись ID
            print(f"Записываем 5 полученных place_id в файл '{self.FILE_NAME}'")
            # Безопасно(with)) пишем(w) со стандартной кодировкой(utf-8) в файл
            with open(self.FILE_NAME, "w", encoding="utf-8") as file:
                for pid in place_ids:  # На каждом шаге берем элемент из списка и записываем его в pid
                    file.write(f"{pid}\n")  # Пишем в файл каждый pid через перенос строки

            # 3) Чтение файла и проверка через GET
            assert os.path.exists(
                self.FILE_NAME
            ), "Ошибка: Файл с ID не был создан!" # Проверка случая, что файл не "записался"

            # Безопасно(with) открываем файл строго для чтения(r) со стандартной кодировкой(utf-8)
            with open(self.FILE_NAME, "r", encoding="utf-8") as file:
                # Читаем строки и очищаем их от лишних невидимых символов:
                loaded_ids = [line.strip() for line in file if line.strip()]  # список place_id

            # Проверяем, что в файле ровно 5 записей
            assert len(loaded_ids) == 5, f"В файле должно быть 5 place_id, но обнаружено {len(loaded_ids)}"

            print(f"Файл '{self.FILE_NAME}' успешно записан и содержит пять place_id")

            get_url = f"{self.BASE_URL}/{self.GET_RESOUSE}"  # путь для GET-запроса

            print(f"Считываем place_id из файла '{self.FILE_NAME}'")
            for idx, pid in enumerate(loaded_ids, 1):
                # idx считаем, начиная с 1
                # В pid каждый раз пишем очередное place_id из файла
                print(f"Проверка {idx}-го (из 5-ти) place_id через GET ({pid})")

                # Формируем параметры запроса:
                # 1) Сделаем копию словаря query_params, чтобы не перезаписать исходный KEY_PARAM
                query_params = self.KEY_PARAM.copy()
                # 2) Берем текущий place_id из переменной pid
                # и записывает его в словарь под ключом "place_id":
                query_params["place_id"] = pid

                # GET-запрос для проверки существования записи о текущем place_id
                get_response = requests.get(get_url, params=query_params)

                # Проверяем, что локация существует по мнению сервера (код ответа 200)
                assert get_response.status_code == 200, (
                    f"Локация с place_id {pid} отсутствует или недоступна! Код ответа: {get_response.status_code}"
                )

                # Проверяем, что в ответе параметр name соответствует place_id из ранее отправленного POST-запроса
                # Имя места для новых place_id, которое должно создаться POST-запросами
                # (по которому косвенно проверим существование новых place_id):
                name_of_place = self.body["name"]

                get_data = get_response.json()  # превращаем ответ от сервера в словарь
                # Получаем значение для name, которое сравниваем с ожидаемым

                assert get_data.get(
                    "name"
                ) == name_of_place, f"Параметр name для place_id {pid} искажен или не совпадает"

            print("Все проверки пройдены успешно")

        finally:  # Блок удаления временного файла при любом исходе теста
            print("\nБудет произведена попытка удаления временного файла")
            if os.path.exists(self.FILE_NAME):
                print(f"Удаление временного файла '{self.FILE_NAME}' произойдёт через 5 секунд")
                time.sleep(6)
                os.remove(self.FILE_NAME)
                if not os.path.exists(self.FILE_NAME):
                    print(f"Временный файл '{self.FILE_NAME}' удален")
                else:
                    print(f"Удаление временного файла '{self.FILE_NAME}' не произведено")
            else:
                print("Временный файл не был создан, удаление не произведено")

            print("-=Конец теста=-")


# Точка запуска скрипта
test = GoogleMapTest()
test.post_get_5_times()