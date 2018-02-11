import time
import sys
import requests
import json
import vk_login


def list2str(arr, start_pos=0, end_pos=0):
    result = ''
    sp = start_pos if start_pos else 1
    ep = end_pos if end_pos else len(arr)
    i = sp - 1
    while i < ep:
        result += str(arr[i]) + ','
        i += 1
    result = result[:-1]
    return result


class VKInterface:

    error = False
    error_msg = ''
    request_count = 0

    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token

    def get_request(self, url, params):

        result = []

        # Ждем секунду и в это время выводим мигающую точку
        if self.request_count == 3:
            for i in range(5):
                sys.stderr.write('\r*')
                time.sleep(0.1)
                sys.stderr.write("\r")
                time.sleep(0.1)
            self.request_count = 0

        response = requests.get(url, params)

        if response.ok:
            response_json = response.json()
            if response_json.get('error'):
                self.error = True
                self.error_msg = response_json['error']['error_msg']
            else:
                result = response_json['response']
        else:
            self.error = True
            self.error_msg = response.content

        return result

    def init_request_param(self):
        params = {
            'access_token': self.access_token,
            'user_id': self.user_id}
        self.error = False
        self.error_msg = ''
        self.request_count += 1
        return params

    def get_friends_list(self):
        params = self.init_request_param()
        return self.get_request('https://api.vk.com/method/friends.get', params)

    def get_groups_list(self):
        params = self.init_request_param()
        return self.get_request('https://api.vk.com/method/groups.get', params)

    def get_groups_details(self, group_id):
        params = self.init_request_param()
        params['group_id'] = group_id
        params['fields'] = 'members_count'
        return self.get_request('https://api.vk.com/method/groups.getById', params)

    def get_members_of_group(self, group_id, user_ids):
        params = self.init_request_param()
        params['user_ids'] = user_ids
        params['group_id'] = group_id
        return self.get_request('https://api.vk.com/method/groups.isMember', params)

    def is_unique_group(self, group_id, friends):

        result = True
        max_friend = 100
        start_pos = 1
        end_pos = min(len(friends), max_friend)
        while True:
            str_friend = list2str(friends, start_pos, end_pos)
            members = self.get_members_of_group(group_id, str_friend)
            if self.error:
                print('Ошибка при получение состава группы: {}. Group_id = {}. Friends = {}'.format(self.error_msg, group_id, str_friend))
                result = None
                break
            for member in members:
                if member['member']:
                    result = False
                    break
            if not result:
                break
            start_pos = end_pos + 1
            if start_pos > len(friends):
                break
            end_pos = min(len(friends), end_pos + max_friend)

        return result


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
print('Группы пользователя: {} шт., {}'.format(len(groups_list), groups_list))

my_groups = []
for group in groups_list:
    uniq = vk_interface.is_unique_group(group, friends_list)
    if uniq:
        group_info = vk_interface.get_groups_details(group)
        if vk_interface.error:
            print('Ошибка при получении сведений по группе {}. Group_id = {}'.format(vk_interface.error_msg, group))
        else:
            my_groups.append(dict(name=group_info[0]['name'], gid=group_info[0]['gid'],
                                  members_count=group_info[0]['members_count']))
    # break

with open('groups.json', 'w') as jfile:
    json.dump(my_groups, jfile)
    sys.stderr.write("\r")
    print('Записан файл: {}'.format(jfile.name))
