from flask import render_template, request, jsonify
from . import main

"""
bp.app_errorhandler:注册在全局
bp.errorhandler:注册在蓝本
"""



@main.app_errorhandler(404)
def page_not_found(e):
    if request.path.startswith("/api"):
        return jsonify({
            "code": 404,
            "msg": "The requested resource is not available",
        })
    return render_template("404.html"),404



@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500