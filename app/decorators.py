from functools import wraps
from flask_login import current_user
from .models import Permission
from flask import abort

def permission_required(permission):
    pass




def admin_required(f):

    @wraps(f)
    def inline_func(*args,**kwargs):
        if not current_user.can(Permission.ADMINISTER):
            abort(403)
        return f(*args,**kwargs)

    return inline_func