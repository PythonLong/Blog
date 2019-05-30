from app import create_app

from app.models import User, Post, Comment

from app import db

app = create_app('default')
app.app_context().push()


import string
import random

def random_title():
    list_chose = ['IG','JDG','EDG','WE','TOP','SDG','RNG','BLG']
    return str(random.choice(list_chose)) + str(random.randint(1,100))



def random_text(n1,n2):
    chars=string.ascii_letters+string.digits
    ranstr=[''.join(random.sample(chars,n1)) for i in range(n2)]
    s='-'.join(ranstr)
    return s




def fake_admin():
    u = User.query.get(1)
    return u

fake = fake_admin()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            author = fake,
            title=random_title(),
            html=random_text(5,5),
            text=random_text(10,10)
        )
        db.session.add(post)
    db.session.commit()




def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author = fake,
            content=random_title(),
            post=Post.query.get(random.randint(1, Post.query.count())),

        )
        db.session.add(comment)

    salt = count*0.1

    for i in range(salt):
        reply = Comment(
            author=fake.name(),
            content=random_title(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
        )
        db.session.add(reply)

    db.session.commit()

if __name__ == '__main__':
    fake_posts()