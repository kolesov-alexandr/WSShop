import flask

from flask import redirect

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.errorhandler(400)
def not_found(error):
    return redirect("/bad_request")


@blueprint.errorhandler(401)
def not_found(error):
    return redirect("/login")


@blueprint.errorhandler(404)
def not_found(error):
    return redirect("/not_found")
