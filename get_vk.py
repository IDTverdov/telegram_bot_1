import requests
import config as cfg


def get_wall_posts():
    group_name = 'group_name'
    count_posts = '5'
    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count={count_posts}&access_token={cfg.TOKEN_VK}&v=5.131'
    req = requests.get(url)
    src = req.json()

    posts = src['response']['items']

    with open('exist_post.txt', 'r') as file:
        old_posts = file.readlines()

    for post in posts:
        send_list = []
        post_id = post['id']
        wall_id = post['from_id']
        if f'{post_id}\n' not in old_posts:
            originalUrl = f'https://vk.com/wall{post_id}_{wall_id}'
            text = [post["text"] + '\n' + originalUrl]
            send_list.append(text)
            url_png = post['attachments'][0]['photo']["sizes"][-1]['url']
            if url_png:
                send_list.append(url_png)

            with open('exist_post.txt', 'a') as file:
                post_id_for_file = f'{post_id}\n'
                file.writelines(post_id_for_file)
    return send_list


def cut_file():
    with open('exist_post.txt', 'r') as file:
        posts = file.readlines()
    posts = posts[-5:]
    with open('exist_post.txt', 'w') as file:
        file.writelines(posts)

