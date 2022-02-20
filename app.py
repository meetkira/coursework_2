from flask import Flask, request, render_template, redirect, url_for
from utils import get_posts_all, get_post_by_pk, get_comments_to_post, search_for_posts, get_posts_by_tag, \
    get_posts_and_tags_by_user, add_post_to_bookmarks, get_bookmarks, get_number_of_bookmarks, delete_bookmark

app = Flask(__name__)


@app.route("/")
def index_page():
    """Главная страница"""
    posts = get_posts_all()
    number_of_bookmarks = get_number_of_bookmarks()
    return render_template('index.html', number_of_bookmarks=number_of_bookmarks, posts=posts)


@app.route("/posts/<int:postid>")
def post_page(postid):
    """Страница с одним постом, найденным по id"""
    post = get_post_by_pk(postid)
    comments, number_of_comments = get_comments_to_post(postid)

    return render_template('post.html', post=post, comments=comments, number_of_comments=number_of_comments)


@app.route("/search/")
def search_page():
    """Страница поиска"""
    s = request.args.get("s")
    if not s or s == "":
        return "Вы ничего не искали"
    posts, number_of_posts = search_for_posts(s)

    return render_template('search.html', posts=posts, number_of_posts=number_of_posts)


@app.route("/users/<string:username>")
def user_page(username):
    """Страница постов пользователя, найденного по имени"""
    user_posts = get_posts_and_tags_by_user(username)

    return render_template('user-feed.html',username=username, user_posts=user_posts)


@app.route("/tag/<string:tagname>")
def tag_page(tagname):
    """Страница постов, найденных по тегу"""
    posts = get_posts_by_tag(tagname)
    tag = f'<a href="/tag/{tagname}">#{tagname}</a>'

    return render_template('tag.html', tag=tag, posts=posts)


@app.route("/bookmarks/add/<int:postid>")
def add_bookmark_page(postid):
    """Добавление страницы в закладки """
    if not add_post_to_bookmarks(postid):
        return "ошибка загрузки"
    return '<script>document.location.href = document.referrer</script>'


@app.route("/bookmarks/delete/<int:postid>")
def delete_bookmark_page(postid):
    """Удаление страницы из закладок """
    if not delete_bookmark(postid):
        return "ошибка удаления"
    return redirect("/bookmarks/", code=302)


@app.route("/bookmarks/")
def bookmarks_page():
    """Добавление страницы в закладки """
    bookmarks = get_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)


if __name__ == "__main__":
    app.run()
