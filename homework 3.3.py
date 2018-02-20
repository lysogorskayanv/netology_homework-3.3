#AUTOREZE_URL = "https://oauth.vk.com/authorize"
#APP_ID = 6217022
#VERSION = "5.68"

#params = {
        #"client_id": APP_ID,
        #"display": "page",
        #"redirect_uri": "https://oauth.vk.com/blank.html",
        #"scope": "friends",
        #"respons_type": "token",
        #"v": VERSION
        #}

#print ('?').join(
        #(AUTOREZE_URL, urlencode(params)
        #))

def find_my_friends(): #поиск моих друзей
    params = {
        'user_id': config.MY_ID,
        'fields': 'first_name',
        'access_token': config.TOKEN,
        'v': config.VERSION,
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    friend_list = response.json().get('response').get('items')
    friend_ids = []
    for person in friend_list:
        friend_ids.append(person["id"])
    set_of_my_friends = set(friend_ids)
    return set_of_my_friends


def find_friends_of_my_friends(set_of_my_friends): #поиск друзей моих друзей
    friends_of_my_friends_list = []
    for user_id in set_of_my_friends:
        params = {
            'user_id': user_id,
            'fields': 'first_name',
            'access_token': config.TOKEN,
            'v': config.VERSION,
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friends_of_my_friends_list.append(response.json().get('response').get('items'))
    friends_of_my_friends_ids = []
    for sublist in friends_of_my_friends_list:
        for person in sublist:
            friends_of_my_friends_ids.append(person["id"])
    set_of_friends_of_my_friends = set(friends_of_my_friends_ids)
    return set_of_friends_of_my_friends


def intersection(set_of_my_friends, set_of_friends_of_my_friends): #поиск пересечений
    common_friends_ids = set_of_my_friends & set_of_friends_of_my_friends
    return common_friends_ids


def output(common_friends_ids): #вывод пересечений
    params = {
        'user_ids': str(common_friends_ids),
        'fields': 'first_name',
        'access_token': config.TOKEN,
        'v': config.VERSION,
    }
    response = requests.get('https://api.vk.com/method/users.get', params)
    common_friends = response.json().get('response')
    print("Мои друзья, которые дружат с миоими друзьями: ")
    for person in common_friends:
            print(person["first_name"], person["last_name"])

if __name__ == "__main__":
    output(intersection(find_my_friends(), find_friends_of_my_friends(find_my_friends())))