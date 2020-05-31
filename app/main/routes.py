from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, NewRecipeForm, SearchRecipeToDelete, DeleteRecipeForm
from app.models import User, Recipe, DishType, Ingredient, Step
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    recipes = current_user.recipes
    return render_template('index.html', title='Home', recipes=recipes)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    recipes = current_user.recipes

    return render_template('user.html', user=user, recipes=recipes)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = NewRecipeForm()
    form.dish_type.choices = [(t.id, t.name) for t in DishType.query.all()]

    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data,
                        description=form.description.data,
                        user_id=current_user.id,
                        dish_type_id=form.dish_type.data)
        db.session.add(recipe)

        ingredients = []
        for d in form.ingredients.data.split(';'):
            d = d.strip()
            if d != '':
                ingredients.append(d)
        for i in ingredients:
            ingredient = Ingredient(name=i, recipe=recipe)
            db.session.add(ingredient)

        steps = []
        for d in form.steps.data.split(';'):
            d = d.strip()
            if d != '':
                steps.append(d)
        for i in steps:
            step = Step(name=i, recipe=recipe)
            db.session.add(step)

        db.session.commit()
        flash('Your recipe has been saved!')
        return redirect(url_for('main.index'))

    return render_template('add_recipe.html', title='Add recipe', form=form)


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = SearchRecipeToDelete()

    if form.validate_on_submit():
        search_string = form.data['recipe_to_delete']
        return redirect(url_for('main.delete_recipe', search_string=search_string))

    return render_template('dashboard.html', title='Dashboard', form=form)


@bp.route('/delete_recipe/<search_string>', methods=['GET', 'POST'])
@login_required
def delete_recipe(search_string):
    search_result = Recipe.query.filter_by(title=search_string).all()
    recipes_count = len(search_result)
    form = DeleteRecipeForm()

    if form.validate_on_submit():
        form_id = int(form.form_id.data)

        Recipe.query.filter_by(id=search_result[form_id].id).delete()
        
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('delete_recipe.html', title='Delete recipe', search_result=search_result,
                           recipes_count=recipes_count, form=form)
