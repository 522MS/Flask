from flask import Blueprint, render_template

from blog.user.views import USERS, get_user

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')

ARTICLES = {
    1: {
        'text': 'abrakadabra',
        'author': 3
    },

    2: {
        'text': 'kabzda',
        'author': 1
    }

}


@article.route('/')
def article_list():
    return render_template(
        'articles/list.html',
        articles=ARTICLES
    )


@article.route('<int:pk>')
def get_article(pk: int):
    article = ARTICLES[pk]
    return render_template(
        'articles/details.html',
        text=article['text'],
        author=USERS[article['author']],
        user_id=article['author']
    )
