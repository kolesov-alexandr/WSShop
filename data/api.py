import flask

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)
# --- Позже появятся новые функции ---
