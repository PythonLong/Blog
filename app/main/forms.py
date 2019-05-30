from wtforms import Form,StringField, SelectField,TextAreaField
from wtforms.validators import Length, DataRequired, ValidationError

from app.models import Role, User


class EditProfileForm(Form):
       username = StringField('Username',validators=[Length(0,64)])


# 管理员能编辑其他人的资料
class EditProfileAdminForm(Form):
    username = StringField('Username',validators=[DataRequired(),Length(0,64)])
    role = SelectField('Role',coerce=int)



    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.current_user = user

    def validate_username(self,field):
        if field.data != self.current_user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class CommentForm(Form):
    content = StringField('content',validators=[DataRequired()])


class PostForm(Form):
    title = StringField('title',validators=[DataRequired()])
    html = TextAreaField(validators=[DataRequired()])
    text = TextAreaField(validators=[DataRequired()])
