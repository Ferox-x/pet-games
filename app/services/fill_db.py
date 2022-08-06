import datetime
from json import dumps
from os import path
from random import randint

fixtures_dir = path.join(path.abspath(__file__), '../../../')


def write_file(file_name, data_list):
    with open(path.join(fixtures_dir, 'fixtures', file_name), 'w',
              encoding='utf-8') as file:
        json_list = dumps(data_list)
        file.write(json_list)


python_list = list()
schulte_list = list()
stroop_list = list()

for index in range(1, 101):
    correct = randint(10, 100)
    incorrect = randint(10, 100)
    all_answers = correct + incorrect
    score = randint(100, 10000)
    record = randint(1000, 10000)

    default_dict_schulte = {
        "model": "games.schultemodel",
        "pk": index,
        "fields": {
            "user": index,
            "record": record,
            "date": "2022-08-05T09:54:36.708Z"
        }
    }

    default_dict_users = {
        "model": "users.users",
        "pk": index,
        "fields": {
            "password": "pbkdf2_sha256$320000$MWT1VCzCYFgQIA3usacJVk$kyHuGLX64nRSDzDSbGmNcnR7o135xgTJBe/qL9/pzac=",
            "last_login": "2022-08-05T05:18:30.323Z",
            "username": f"User{index}",
            "country": "",
            "description": None,
            "email": None,
            "first_name": None,
            "last_name": None,
            "is_active": True,
            "is_admin": False,
            "is_superuser": False,
            "groups": [],
            "user_permissions": []
        }
    }

    default_dict_stroop = {
        "model": "games.stroopmodel",
        "pk": index,
        "fields": {
            "user": index,
            "record": f"{correct} - {incorrect} - {all_answers}",
            "score": score,
            "date": "2022-08-05T05:18:40.794Z"
        }
    }

    python_list.append(default_dict_users)
    schulte_list.append(default_dict_schulte)
    stroop_list.append(default_dict_stroop)

write_file('user.json', python_list)
write_file('schulte_leaderboard.json', schulte_list)
write_file('stroop_leaderboard.json', stroop_list)
