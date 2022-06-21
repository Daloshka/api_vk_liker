import time
import database
import vk_api
import random
import requests
from info import api_key, server_ip

while True:
    print("Ожидание запроса")
    try:
        print("Ожидание ответа от сервера")
        request = requests.get(f"http://{server_ip}/task/getNewTasks?key={api_key}")
        rs = request.json()['response']
        for r in rs:
            try:
                id_task = r['id'] # int
                if (r['data_request'] != None):
                    data_request = r['data_request']
                    type_task = data_request['type'] # string
                    owner_id = data_request['owner_id'] # int
                    item_id = data_request['item_id'] # int
                    count = r['count'] # int
                    payInfo = r['type'] # string
                    database.add_task(id_task, type_task, owner_id, item_id, count, payInfo)
                    print(f'Задача добавлена id_task: {id_task}, count: {count}, type_task: {type_task}, owner_id: {owner_id}, payInfo: {payInfo}')
                else:
                    print("data NONE")
                    pass
            except Exception as ex:
                print(f"Error 'r in rs' {ex}")
        print('Запросы приняты')
    except Exception as ex:
        print(f"Error in GET_TASKS {ex}")
    print("Запрос принят")

    