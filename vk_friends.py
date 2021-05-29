import requests
from requests.exceptions import ConnectionError
import socket
from urllib3.exceptions import NewConnectionError, MaxRetryError


URL_FRIENDS_GET = 'https://api.vk.com/method/friends.get'
URL_USERS_GET = 'https://api.vk.com/method/users.get'
TOKEN = 'f321f289c91e15f4010a2dfc3e15093e735b7e7485c' \
        '06cce3ae05f6109c60b99dfb977a10389fd9a17b22'
FIELDS = {
    'last_name': lambda x: str(x),
    'first_name': lambda x: str(x),
    'online': lambda x: '[Online]' if x == 1 else '[Offline]'
}
API_VERSION = '5.52'


def main():
    user_id = input('Введите id пользователя, '
                    'друзей которого вы хотите найти: ')

    try:
        try:
            int(user_id)
        except ValueError:
            response_user = requests.get(URL_USERS_GET, params={
                'access_token': TOKEN,
                'user_ids': user_id,
                'v': API_VERSION
            })
            try:
                user_id = response_user.json()['response'][0]['id']
            except (ValueError, KeyError, UnboundLocalError):
                print(f'Произошла ошибка при попытке получения данных о '
                      f'пользователе [Id="{user_id}"]! Пожалуйста правильность '
                      f'введенных вами данных.')
                return

        response_friends = requests.get(URL_FRIENDS_GET, params={
            'access_token': TOKEN,
            'user_id': user_id,
            'fields': ','.join(FIELDS),
            'v': API_VERSION
        })
    except (socket.gaierror, NewConnectionError, MaxRetryError, ConnectionError):
        print('Произошла ошибка при подключении! '
              'Пожалуйста проверьте ваше соединение с интернетом.')
        return

    if 'error' in response_friends.json().keys():
        print(f'Произошла ошибка при попытке получения данных о '
              f'пользователе [Id="{user_id}"]! Пожалуйста правильность '
              f'введенных вами данных.')
        return

    print(f'Найдено {response_friends.json()["response"]["count"]} друзей:')
    for item in response_friends.json()['response']['items']:
        print(' '.join(func(item[field]) for field, func in FIELDS.items()))


if __name__ == '__main__':
    main()
