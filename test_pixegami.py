import requests,uuid

ENDPOINT = "https://todo.pixegami.io/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    payload = new_task_payload()
    create_response = create_task(payload)
    assert create_response.status_code == 200

    data = create_response.json()
    task_id = data["task"]["task_id"]

    get_response = get_task(task_id)
    assert get_response.status_code == 200

    get_data = get_response.json()
    assert get_data["content"] == payload["content"]
    assert get_data["user_id"] == payload["user_id"]


def test_can_update_task():
    payload = new_task_payload()
    create_response = create_task(payload)
    assert create_response.status_code == 200

    task_id = create_response.json()["task"]["task_id"]

    new_payload = {
    "user_id": payload["user_id"],
    "task_id": task_id,
    "content": "TEST 2",
    "is_done": True,   
   }

    update_response = update_task(new_payload)
    assert update_response.status_code == 200

    new_response = get_task(task_id)
    update_response_data = new_response.json()
    assert update_response_data["content"] == new_payload["content"]    
    assert update_response_data["is_done"] == new_payload["is_done"]
    assert update_response_data["user_id"] == new_payload["user_id"]
    assert update_response_data["task_id"] == new_payload["task_id"]


def test_can_list_tasks():
    n=5
    payload = new_task_payload()
    for i in range(n):
        create_response = create_task(payload)
        assert create_response.status_code == 200
 
    user_id = payload["user_id"]
    list_response = list_user(user_id)
    assert list_response.status_code == 200

    list_data = list_response.json()
    data = list_data["tasks"]
    assert len(data) == n
   

def test_can_delete_task():
    payload = new_task_payload()
    create_response = create_task(payload)
    assert create_response.status_code == 200

    task_id = create_response.json()["task"]["task_id"]

    delete_response = delete_task(task_id)
    assert delete_response.status_code == 200

    get_response = get_task(task_id)
    assert get_response.status_code == 404
    











def create_task(payload):
    return requests.put(ENDPOINT + "create-task", json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + "get-task/" + task_id)

def update_task(payload):
    return requests.put(ENDPOINT + "update-task/",  json=payload)

def list_user(user_id):
    return requests.get(ENDPOINT + "list-tasks/" + user_id)

def delete_task(task_id):
    return requests.delete(ENDPOINT + "delete-task/" + task_id)

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    return {
            "content": "TEST",
            "user_id": user_id,
            "task_id": "test id",
            "is_done": False, }