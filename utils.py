import json

POST_PATH = "data/data.json"
COMMENT_PATH = "data/comments.json"
BOOKMARK_PATH = "data/bookmarks.json"


def _open_json(filename):
    """Открытие json-файла"""
    with open(filename, encoding='utf-8') as f:
        json_data = json.load(f)

    return json_data


def _save_to_json(filename, post):
    """Сохранение поста в json-файл"""
    json_data = _open_json(filename)
    json_data.append(post)

    try:
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
    except Exception:
        return False

    return True


def _save_all_to_json(filename, posts):
    """Переписать json-файл полностью(при удалении поста)"""
    try:
        with open(filename, 'w') as f:
            json.dump(posts, f, indent=4)
    except Exception:
        return False

    return True


def _find_in_json(filename, pk):
    """Проверка есть ли пост в файле"""
    json_data = _open_json(filename)
    for post in json_data:
        if post["pk"] == pk:
            return True
    return False


def get_posts_all():
    """Получение всех постов"""
    return _open_json(POST_PATH)


def _get_posts_by_user(user_id):
    """Получение постов пользователя по его id"""
    json_data = _open_json(POST_PATH)
    posts = [post for post in json_data if post["poster_name"] == user_id]

    return posts


def search_for_posts(query):
    """Поиск постов по параметру в содержании"""
    json_data = _open_json(POST_PATH)
    posts = [post for post in json_data if query in post["content"].lower()]
    number_of_posts = len(posts)

    return posts, number_of_posts


def get_post_by_pk(pk):
    """Получение поста по id"""
    json_data = _open_json(POST_PATH)

    return json_data[pk - 1]


def get_comments_to_post(pk):
    """Получение количества комментариев к посту по id"""
    json_data = _open_json(COMMENT_PATH)
    comments = [comment for comment in json_data if comment["post_id"] == pk]
    number_of_comments = len(comments)
    last_digit = number_of_comments % 10
    if 11 <= number_of_comments <= 19:
        comments_ending = " комментариев"
    elif last_digit == 1:
        comments_ending = " комментарий"
    elif 2 <= last_digit <= 4:
        comments_ending = " комментария"
    else:
        comments_ending = " комментариев"

    number_of_comments = str(number_of_comments) + comments_ending

    return comments, number_of_comments


def get_posts_by_tag(tag):
    """Получение постов по тегу"""
    json_data = _open_json(POST_PATH)
    posts = []
    for item in json_data:
        text = item["content"].split()
        for word in text:
            if word.startswith("#"):
                if word.translate({ord(i): None for i in '#!,.?'}) == tag:
                    posts.append(item)

    return posts


def _get_tags_by_user_posts(posts):
    """Получение тегов для каждого поста пользователя"""
    for post in posts:
        text = post["content"].split()
        post["tags"] = []
        for word in text:
            if word.startswith("#"):
                word = word.translate({ord(i): None for i in '#!,.?'})
                tag = f'<a href="/tag/{word}">#{word}</a>'
                post["tags"].append(tag)

    return posts


def get_posts_and_tags_by_user(user_id):
    """Получение тегов и постов пользователя"""
    posts = _get_posts_by_user(user_id)
    posts = _get_tags_by_user_posts(posts)

    return posts


def add_post_to_bookmarks(pk):
    """Добавление поста в закладки"""
    post = get_post_by_pk(pk)
    if _find_in_json(filename=BOOKMARK_PATH, pk=pk):
        return True
    if not _save_to_json(filename=BOOKMARK_PATH, post=post):
        return False
    return True


def get_bookmarks():
    """Получение постов, добавленных в закладки"""
    bookmarks = _open_json(BOOKMARK_PATH)

    return bookmarks


def get_number_of_bookmarks():
    """Получение количества постов, находящихся в закладках"""
    bookmarks = get_bookmarks()
    number_of_bookmarks = len(bookmarks)

    return number_of_bookmarks


def delete_bookmark(pk):
    """Удаление закладки"""
    current_bookmarks = get_bookmarks()
    bookmarks = [bookmark for bookmark in current_bookmarks if pk != bookmark['pk']]
    if not _save_all_to_json(filename=BOOKMARK_PATH, posts=bookmarks):
        return False
    return True
