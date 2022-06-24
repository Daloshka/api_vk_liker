import time
import database
import vk_api
import random
import requests
from info import api_key, server_ip

def update_max_likes(max_likes = 250):
    r = requests.get(f"http://{server_ip}/counter/setAccountCount?key={api_key}&amount={max_likes}")
    if (r.status_code == 200 and r.json()['response'] == 1):
        print("Обновленно успешно")

def get_tasks():
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


def task_done(task_id):
    r = requests.get(f"http://{server_ip}/task/done?key={api_key}&task_id={int(task_id)}")    

def like():
    try:
        task = database.get_task()
        id_task, type_task, owner_id, item_id, count, payInfo = task
        tokens = database.get_active_tokens()
        likes_done = 0
        counter_tokens = 0
        length_tokens = len(tokens)
        for token in tokens:
            try:
                session = vk_api.VkApi(token= token)
                if (session.method('likes.isLiked', {'owner_id' :owner_id, 'item_id': item_id,'type':type_task, 'random_id' : random.randint(1000, 99999)})['liked'] != 1):
                    print(f"owner_id' :{owner_id}, 'post_id': {item_id}")
                    session.method('likes.add', {'owner_id' :owner_id, 'item_id': item_id,'type':type_task, 'random_id' : random.randint(1000, 99999)})
                    print("+", end="")
                    likes_done += 1
                    counter_tokens += 1
                    print(f"likes_done {likes_done} count {count} progress {counter_tokens}/{length_tokens}")
                    if (int(count) == int(likes_done)):
                        database.delete_task(id_task)
                        task_done(id_task)
                        time.sleep(5)
                        print("Задание выполнено!")
                        break
            except:
                counter_tokens += 1
                print(f"- {counter_tokens}/{length_tokens}\n", end='')
    except Exception as ex:
        print(f"Error in LIKE {ex}")


while True:
    try:
        like()
        time.sleep(40)
    except Exception as ex:
        print(f"Error in WHILE TRUE {ex}")
