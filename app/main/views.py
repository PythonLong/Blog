from flask import render_template, url_for, abort, request, flash, redirect, send_from_directory, current_app,jsonify
from flask_login import login_required, current_user
from json import loads
from app.decorators import admin_required
from app.main.forms import EditProfileForm, EditProfileAdminForm, CommentForm, PostForm
from . import main
from .. import db
from ..models import User, Role, Post, Comment, Permission

from datetime import datetime

@main.route("/",methods=["GET","POST"])
def index():
    page = request.args.get('page', 1, type=int) #当前页数
    pagination = Post.query.filter_by(display=True).order_by(Post.time.desc()).paginate(page,per_page=current_app.config['POSTS_PER_PAGE'])
    posts = pagination.items

    return render_template("index.html",posts=posts,pagination=pagination)


#资料页中显示博客文章
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.oder_by(Post.time.desc()).all()
    return render_template('user.html',user=user,posts=posts)


@main.route('/edit_profile',methods=['GET',"POST"])
@login_required
def edit_profile():
    form = EditProfileForm(formdata=request.form)
    if request.method == 'POST':
        if form.validate():
            current_user.username = form.username.data
            db.session.add(current_user)
            flash('Your profile has been updated.')
            return redirect(url_for('main.user', username=current_user.username))

    form.username.data = current_user.username
    return render_template('edit-profile',form=form)

@main.route('/admin')
@login_required
@admin_required
def admin_page():
    return "For administrators!"

@main.route('/edit_profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if request.method == 'POST':
        if form.validate():
            user.username = form.username.data
            user.role_id  = Role.query.get(form.role.data)
            db.session.add(user)
            flash('The profile has been updated.')
            return redirect(url_for('.user', username=user.username))

    form.username.data = user.username
    form.role.data = user.role_id
    return render_template('edit_profile.html',form=form,user=user)

#写博客
@main.route('/edit_post',methods=["GET","POST"])
@login_required
def edit_post():
    if request.method == "POST":
        result = {"status":200,'msg':"success"}
        form = PostForm(request.form)
        if form.validate():
            tags = loads(request.form.get('taginfo',None))
            post = Post(title=form.title.data, text=form.text.data, html=form.html.data,author=current_user._get_current_object())
            if tags:
                post.tag = tags
            db.session.add(post)
            db.session.commit()
        else:
            result['status'] = 400
            result['msg'] = form.errors

        return jsonify(result),result['status']
    return render_template("edit_post.html")


#修改博客
@main.route('/edit_post/<int:id>',methods=["GET","POST"],endpoint="change")
@login_required
def change_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER): #不是 (作者|管理员)
        abort(403)

    if request.method == "POST":
        form = PostForm(request.form)
        if form.validate():
            post.tag = loads(request.form.get('taginfo', None))
            post.title = form.title.data
            post.text = form.text.data
            post.html = form.html.data
            db.session.add(post)
            db.session.commit()
            return jsonify({
                "msg":"success"
            }),200
        else:
            return jsonify({
                "msg":"data error"
            }),400

    return render_template('change_post.html',post=post)


#管理博客页面
@main.route('/manage',endpoint='manage',methods=["GET","POST"])
@login_required
def manage_post():
    if request.method == "GET":
        posts = current_user.posts.filter_by(display=True).order_by(Post.time.desc()).all()
        return render_template("manage.html",posts=posts)
    else:
        post_id = request.form.get("id")
        #print(type(current_user.posts))
        post = current_user.posts.filter_by(id=post_id).first_or_404()
        post.display = False
        db.session.commit()
        return jsonify({'msg':"success"}),200

#博客详细  在此可以评论
@main.route('/post/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)
    if request.method == "POST":
        form = CommentForm(formdata=request.form)
        if form.validate():
            comment = Comment(content=form.content.data,post=post,author=current_user._get_current_object())
            db.session.add(comment)
            return redirect(url_for('main.post', id=post.id))
    else:
        return render_template("post.html",post=post)


@main.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)