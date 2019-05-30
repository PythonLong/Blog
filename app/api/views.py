from . import api
from flask_login import login_required,current_user
from flask import jsonify
# from collections import Iterable
# from .. import db


@api.route('fans-list',methods=["GET"])
@login_required
def get_fans():
    List = [{"username":item.username,"avatar":item.avatar_s} for item in current_user.follow_fans ]
    result = {
        "code":200,
        "total": len(List),
        "data":{
            "list": List,
        }
    }
    return jsonify(result)

@api.route('follow-list',methods=["GET"])
@login_required
def get_follow():
    # TODO APi
    List = [{"username": item.username, "avatar": item.avatar_s} for item in current_user.follow_star]
    result = {
        "code": 200,
        "total":len(List),
        "data": {
            "list": List,
        }
    }
    return jsonify(result)

@api.route('profile',methods=["GET"])
@login_required
def get_profile():
    result = {
        "code":200,
        "data":{
                "username":current_user.username,
                "since":current_user.since,
                "last":current_user.last,
                "avatar":current_user.avatar_l,
            }
    }
    return jsonify(result)
