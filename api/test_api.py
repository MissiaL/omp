import time
from contextlib import contextmanager
from itertools import product

import pendulum
import pytest

valid_emails = ['valid@mail.ru']
invalid_emails = ['invalid']

valid_names = ['fsdfds', 'fsdf_dfsf', 'Мое имя']
invalid_names = ['', None]

valid_time = ['1d', '1s', '1h', '1m']
invalid_time = [time.time(), -1, '2123123', 1]

valid_comments = ['hi', '!']
invalid_comments = [True, '']

all_valid = valid_emails + valid_names + valid_time + valid_comments
all_invalid = invalid_emails + invalid_names + invalid_time + invalid_comments

all_prepared_combinations = [
    valid_emails + invalid_emails, valid_names + invalid_names, valid_time + invalid_time,
    valid_comments + invalid_comments
]


@contextmanager
def does_not_raise():
    yield


# В итоге в параметризацию попадает вот такой результат
# [('valid@mail.ru', 'fsdfds', '1d', 'hi', Exception or Not), ('valid@mail.ru', 'fsdfds', '1d', '!', Exception or Not), ...]
# Где первые 4 элемента - это email, name, time, comment
# Последний элемент - это ожидаемый результат теста
combinations = []
for data in product(*all_prepared_combinations):
    params = list(data)
    if any(x in data for x in all_invalid):
        params.append(pytest.raises(Exception))
        combinations.append(tuple(params))
    else:
        params.append(does_not_raise())
        combinations.append(tuple(params))


@pytest.fixture(scope='session', autouse=True)
def cleanup(sub):
    yield
    sub.delete()


@pytest.mark.parametrize("email, name, _time, comment, expected", combinations)
def test_create_sub(sub, email, name, _time, comment, expected):
    """ Проверим тут создание подписок с разными типами данных
    """
    with expected:
        sub.create({
            'email': email,
            'name': name,
            'time': _time,
            'comment': comment
        })


def test_get_and_delete_sub(sub):
    """ Проверим, что подписка вприципе нормально создается и отдает ответ
    """
    expired_at = '1d'
    new_sub = {
        'email': 'valid@mail.ri',
        'name': 'name',
        'time': expired_at,
        'comment': 'new coment'
    }
    response = sub.create(new_sub)
    sub_id = response['id']
    assert isinstance(sub_id, str)
    subs = sub.get()
    assert len(subs) == 1
    got_sub = subs[0]
    assert got_sub['email'] == new_sub['email']
    assert got_sub['name'] == new_sub['name']
    created_at = pendulum.parse(got_sub['created_at']).timestamp()
    expired_at = pendulum.parse(got_sub['expired_at']).timestamp()
    assert int(expired_at - created_at) in [86400, 86399]  # 1d
    assert got_sub['comment'] == new_sub['comment']
    assert got_sub['id'] == sub_id

    sub.delete()
    subs = sub.get()
    assert len(subs) == 0
