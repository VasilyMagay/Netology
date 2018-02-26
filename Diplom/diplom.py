import time
import sys
import requests
import json
import vk_login

TOO_MANY_REQUESTS = 6
MAX_GROUP_SIZE = 100


class VKInterface:

    error = False
    error_msg = ''

    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token

    def get_request(self, url, params=None):

        result = []

        request_params = {
            'v': '5.73',
            'access_token': self.access_token,
            'user_id': self.user_id}
        if params:
            request_params.update(params)

        while True:

            too_many_requests = False
            self.error = False
            self.error_msg = ''

            response = requests.get(url, request_params)

            if response.ok:
                response_json = response.json()
                if response_json.get('error'):
                    self.error = True
                    self.error_msg = response_json['error']['error_msg']
                    too_many_requests = int(response_json['error']['error_code']) == TOO_MANY_REQUESTS
                else:
                    result = response_json['response']
            else:
                self.error = True
                self.error_msg = response.content

            if not too_many_requests:
                break

            # Делаем задержку в 0.2 с. для вывода мигающей точки
            sys.stderr.write('\r*')
            time.sleep(0.2)
            sys.stderr.write('\r')

        return result

    def get_friends_list(self):
        return self.get_request('https://api.vk.com/method/friends.get')

    def get_groups_list(self):
        params = {
            'extended': 1,
            'fields': 'members_count'
        }
        return self.get_request('https://api.vk.com/method/groups.get', params)

    def check_members_of_group(self, group_id, user_ids):
        params = {
            'user_ids': user_ids,
            'group_id': group_id
        }
        return self.get_request('https://api.vk.com/method/groups.isMember', params)

    def is_unique_group(self, group_id, friends):

        result = True
        start_pos = 0
        end_pos = MAX_GROUP_SIZE
        while True:
            str_friend = ','.join(str(elem) for elem in friends[start_pos:end_pos])
            members = self.check_members_of_group(group_id, str_friend)
            if self.error:
                print('Ошибка при получение состава группы: {}. Group_id = {}. Friends = {}'.format(self.error_msg, group_id, str_friend))
                result = None
                break
            for member in members:
                if member['member']:
                    return False
            start_pos += MAX_GROUP_SIZE
            if start_pos > len(friends) - 1:
                break
            end_pos += MAX_GROUP_SIZE

        return result


def main():

    vk_interface = VKInterface(vk_login.VK_ID, vk_login.VK_TOKEN)

    friends_list = vk_interface.get_friends_list()
    if vk_interface.error:
        print('Ошибка при получении списка друзей для пользователя с ID {}'.format(vk_interface.user_id))
        sys.exit()

    groups_list = vk_interface.get_groups_list()
    if vk_interface.error:
        print('Ошибка при получении списка групп для пользователя с ID {}'.format(vk_interface.user_id))
        sys.exit()

    friends_list = friends_list['items']
    groups_list = groups_list['items']

    print('Друзья пользователя: {} шт., {}'.format(len(friends_list), friends_list))
    print('Группы пользователя: {} шт., {}'.format(len(groups_list), groups_list))

    my_groups = []
    for group in groups_list:
        if vk_interface.is_unique_group(group['id'], friends_list):
            my_groups.append(dict(name=group['name'], gid=group['id'],
                                  members_count=group['members_count']))

    with open('groups.json', 'w') as jfile:
        json.dump(my_groups, jfile)
        print('Записан файл: {}'.format(jfile.name))


if __name__ == '__main__':
    main()
