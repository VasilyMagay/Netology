import time
import sys
import requests
import json
import vk_login


class VKInterface:

    error = False
    error_msg = ''

    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token

    def get_request(self, url, params=None):

        result = []

        request_params = {
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
                    too_many_requests = (int(response_json['error']['error_code']) == 6)
                else:
                    result = response_json['response']
            else:
                self.error = True
                self.error_msg = response.content

            if too_many_requests:
                # Ждем секунду и в это время выводим мигающую точку
                for i in range(5):
                    sys.stderr.write('\r*')
                    time.sleep(0.1)
                    sys.stderr.write('\r')
                    time.sleep(0.1)
            else:
                break

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
        max_friend = 100
        start_pos = 1
        end_pos = min(len(friends), max_friend)
        while True:
            str_friend = list2str(friends, start_pos, end_pos)
            members = self.check_members_of_group(group_id, str_friend)
            if self.error:
                print('Ошибка при получение состава группы: {}. Group_id = {}. Friends = {}'.format(self.error_msg, group_id, str_friend))
                result = None
                break
            for member in members:
                if member['member']:
                    return False
            start_pos = end_pos + 1
            if start_pos > len(friends):
                break
            end_pos = min(len(friends), end_pos + max_friend)

        return result


def list2str(arr, start_pos=0, end_pos=0):
    sp = start_pos if start_pos else 1
    ep = end_pos if end_pos else len(arr)
    return ','.join(str(elem) for elem in arr[sp-1:ep])


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

    print('Друзья пользователя: {} шт., {}'.format(len(friends_list), friends_list))
    print('Группы пользователя: {} шт., {}'.format(len(groups_list)-1, groups_list[1:]))

    my_groups = []
    for group in groups_list[1:]:
        if vk_interface.is_unique_group(group['gid'], friends_list):
            my_groups.append(dict(name=group['name'], gid=group['gid'],
                                  members_count=group['members_count']))

    with open('groups.json', 'w') as jfile:
        json.dump(my_groups, jfile)
        # sys.stderr.write("\r")
        print('Записан файл: {}'.format(jfile.name))


if __name__ == '__main__':
    main()
