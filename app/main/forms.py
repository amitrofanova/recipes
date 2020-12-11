from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, HiddenField, FileField
from wtforms.fields.html5 import SearchField
from wtforms.validators import ValidationError, DataRequired, Length, regexp
from app.models import User
from flask import request
import os
from flask_babel import lazy_gettext as _l


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))


class NewRecipeForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(min=1, max=140)])
    description = TextAreaField(_l('Description'))
    dish_type = SelectField(_l('Dish type'), coerce=int)
    ingredients = TextAreaField(_l('Add ingredients (please type every ingredient with new line)'))
    steps = TextAreaField(_l('Add steps (please start to type every step from new line)'))
    image_url = HiddenField('Image Url')
    submit = SubmitField(_l('Save recipe'))


class SearchRecipeForm(FlaskForm):
    form_name = HiddenField('Form_name')
    recipe_name = SearchField('Recipe name')
    submit = SubmitField('Find recipe')


class DeleteRecipeForm(FlaskForm):
    form_id = HiddenField('Form_id')
    submit = SubmitField('Delete recipe')


class AddIdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    description = TextAreaField('Description')
    submit = SubmitField('Add idea')

class AddDishTypeForm(FlaskForm):
    dish_type = StringField('Dish type', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Add dish type')
