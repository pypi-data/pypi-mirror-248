from flask import Blueprint, abort
from flask_login import current_user, logout_user

bp = Blueprint('workbench', __name__, url_prefix='/api/workbench')

from . import routes


@bp.before_request
def loginInterceptor():
    if current_user.is_authenticated is False or current_user.user_status == 0 or current_user.is_delete == 1:
        logout_user()
        abort(401)

