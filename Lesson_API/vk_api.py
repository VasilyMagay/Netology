from urllib.parse import urlencode
import requests


def get_my_vk_url():
    app_id = 6287952
    auth_url = 'https://oauth.vk.com/authorize'
    url_data = {
        'client_id': app_id,
        'redirect_uri': 'https://oath.vk.com/blank.html',
        'display': 'page',
        'scope': 'friends',
        'response_type': 'token',
        'v': '5.69'
    }
    return '?'.join((auth_url, urlencode(url_data)))


def get_friend_list(user_id, access_token):
    params = {
        'access_token': access_token,
        'user_id': user_id
    }
    response_vk = requests.get('https://api.vk.com/method/friends.get', params)
    return response_vk.json()['response']


def common_friends(user_id1, user_id2, token):
    friend_list1 = get_friend_list(user_id1, token)
    friend_list2 = get_friend_list(user_id2, token)
    set_friends = set(friend_list1) & set(friend_list2)
    if not len(set_friends):
        print('У пользователей с id {} и {} нет общих друзей'.format(user_id1, user_id2))
    else:
        params = {
            'user_ids': set_friends,
            'fields': 'domain'
        }
        response_vk = requests.get('https://api.vk.com/method/users.get', params)
        print('Общие друзья:')
        response = response_vk.json()['response']
        for user in response:
            print('id: {}, url: {}'.format(user['uid'], ''.join(('https://vk.com/', user['domain']))))


# print(get_my_vk_url())
TOKEN = ''

common_friends(228326959, 228326959, TOKEN)


