from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.fields.html5 import SearchField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class NewRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    description = TextAreaField('Description')
    dish_type = SelectField('Dish type', coerce=int)
    ingredients = TextAreaField('Add Ingredients (please use semicolon as separator)')
    steps = TextAreaField('Add Steps (please use semicolon as separator)')
    submit = SubmitField('Save recipe')


class SearchRecipeToModify(FlaskForm):
    form_name = HiddenField('Form_name')
    recipe_to_modify = SearchField('Name of recipe to modify')
    submit = SubmitField('Find recipe')


class SearchRecipeToDelete(FlaskForm):
    recipe_to_delete = SearchField('Name of recipe to delete')
    submit = SubmitField('Find recipe')


class DeleteRecipeForm(FlaskForm):
    form_id = HiddenField('Form_id')
    submit = SubmitField('Delete recipe')
