from datetime import datetime

from flask_avatars import Identicon

from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Permission():
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User',backref='role',lazy='dynamic')

    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    @staticmethod
    def insert_roles():                #---  生成角色数据  插入角色
        # 取位移或的值

        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (
            Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    # 增加权限
    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions += perm

    # 移除权限
    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # 重置权限
    def reset_permission(self):
        self.permissions = 0

    # 有否由此权限
    def has_permission(self,perm):
        return self.permissions & perm == perm


    def __repr__(self):
        return "<Role %s>" % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    #关注者
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)

    #被关注者
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)

    time = db.Column(db.DateTime,default=datetime.now)


class User(UserMixin,db.Model):

    __tablename__ = 'users'

    #是否验证邮箱
    confirmed = db.Column(db.Boolean,default=False)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    since = db.Column(db.DateTime(),default=datetime.now)
    last = db.Column(db.DateTime(),default=datetime.now)

    #随机头像 字符串
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))


    #文章
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    #评论
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    #关注
    #我关注的人
    follow_star = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                                  backref=db.backref('follower',lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')

    #我的关注粉丝
    follow_fans = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                  backref=db.backref('followed',lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)

        self.set_role()
        self.generate_avatar()


    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['BLUELOG_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()


    # 设置密码属性为不可读
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    #设置密码 计算哈希值
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    #验证密码
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #生成一个令牌，有效期默认为一小时。
    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    #检验令牌，如果检验通过，则把新添加的 confirmed 属性设为 True
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    #confirm() 方法还检查令牌中的 id 是否和存储在 current_user 中的已登录 用户匹配。
    # 如此一来，即使恶意用户知道如何生成签名令牌，也无法确认别人的账户

    def generate_reset_token(self,expiration=3600):   #---生成一个忘记密码的令牌
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')


    @staticmethod
    def reset_password(token,new_password):           # 验证令牌并设置新密码
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def can(self,permission):
        return self.role is not None and \
               (self.role.permissions & permission) == permission

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # 最后活跃时间
    def ping(self):
        self.last = datetime.now()
        db.session.add(self)
        db.session.commit()

    #生成头像
    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s,self.avatar_m,self.avatar_l = filenames[0],filenames[1],filenames[2]
        #30 100 200

        db.session.commit()

    #关注
    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            db.session.commit()

    #取关
    def unfollow(self,user):
        f = Follow.filter_by(followed_id = user.id).first()
        if f:
            db.session.delete(f)

    #是否正在关注中(星)
    def is_following(self,user):
        return bool(self.follow_star.filter_by(followed_id=user.id).first())

    #是否被关注(粉丝)
    def is_followed(self,user):
        return bool(self.follow_fans.filter_by(follower_id=user.id).first())

    def __repr__(self):
        return "<User %s>" % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    html = db.Column(db.Text)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    tag = db.Column(db.PickleType)
    display = db.Column(db.Boolean,default=True)

    #评论
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    #评论数
    com_num = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Post {}: [title:{}, tag:{}]>'.format(self.id, self.title, self.tag)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime,default=datetime.now)
    display = db.Column(db.Boolean,default=True)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

    replied_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    #ed 父对象
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all')




