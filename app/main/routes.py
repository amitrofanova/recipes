from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db, store
from app.main.forms import EditProfileForm, NewRecipeForm, SearchRecipeForm, DeleteRecipeForm
from app.models import User, Recipe, DishType, Ingredient, Step
from app.main import bp
from sqlalchemy_imageattach.context import (pop_store_context, push_store_context)
from werkzeug.utils import secure_filename
import os


@bp.before_request
def start_implicit_store_context():
    push_store_context(store)


@bp.teardown_request
def stop_implicit_store_context(exception=None):
    pop_store_context()


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


@bp.route('/recipe/<recipe_id>')
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()

    return render_template('recipe.html', recipe=recipe)


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
    print(request.files)

    if form.validate_on_submit():
        file = request.files['picture']

        # if 'picture' not in request.files:
        #     return redirect(request.url)
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)

        recipe = Recipe(title=form.title.data,
                        description=form.description.data,
                        user_id=current_user.id,
                        dish_type_id=form.dish_type.data)

        recipe.picture.from_file(file)

        recipe.picture.generate_thumbnail(width=150, store=store)

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
            step = Step(content=i, recipe=recipe)
            db.session.add(step)

        db.session.commit()
        flash('Your recipe has been saved!')
        return redirect(url_for('main.index'))

    return render_template('add_recipe.html', title='Add recipe', form=form)


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = SearchRecipeForm()

    if form.validate_on_submit():
        form_name = form.form_name.data
        search_string = form.data['recipe_name']

        if form_name == 'modify':
            return redirect(url_for('main.modify_recipe', search_string=search_string))

        if form_name == 'delete':
            return redirect(url_for('main.delete_recipe', search_string=search_string))

    return render_template('dashboard.html', title='Dashboard', form=form)


@bp.route('/delete_recipe/<search_string>', methods=['GET', 'POST'])
@login_required
def delete_recipe(search_string):
    search_result = Recipe.query.filter_by(title=search_string).filter_by(user_id=current_user.id).all()
    recipes_count = len(search_result)

    if not recipes_count:
        flash('Recipes not found')
        return redirect(url_for('main.dashboard'))

    form = DeleteRecipeForm()

    if form.validate_on_submit():
        form_id = int(form.form_id.data)

        Recipe.query.filter_by(id=search_result[form_id].id).delete()

        db.session.commit()
        flash('Recipe has been deleted')
        return redirect(url_for('main.index'))

    return render_template('delete_recipe.html', title='Delete recipe', search_result=search_result,
                           recipes_count=recipes_count, form=form)


@bp.route('/modify_recipe/<search_string>', methods=['GET', 'POST'])
@login_required
def modify_recipe(search_string):
    search_result = Recipe.query.filter_by(title=search_string).filter_by(user_id=current_user.id).first()

    if not search_result:
        flash('Recipes not found')
        return redirect(url_for('main.dashboard'))

    form = NewRecipeForm()
    form.dish_type.choices = [(t.id, t.name) for t in DishType.query.all()]

    if form.validate_on_submit():
        recipe = Recipe.query.filter_by(id=search_result.id).first_or_404()

        ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()
        for i in ingredients:
            Ingredient.query.filter_by(id=i.id).delete()

        steps = Step.query.filter_by(recipe_id=recipe.id).all()
        for s in steps:
            Step.query.filter_by(id=s.id).delete()

        file = request.files['picture']
        recipe.picture.from_file(file)
        recipe.picture.generate_thumbnail(width=150, store=store)

        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.dish_type_id = form.dish_type.data

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
            step = Step(content=i, recipe=recipe)
            db.session.add(step)

        db.session.commit()
        flash('Your recipe has been saved!')
        return redirect(url_for('main.index'))

    elif request.method == 'GET':
        form.title.data = search_result.title
        form.description.data = search_result.description
        form.dish_type.data = search_result.dish_type_id

        ingredients = ''
        for i in search_result.ingredients:
            ingredients += i.name
            ingredients += ';\n'
        form.ingredients.data = ingredients

        steps = ''
        for s in search_result.steps:
            steps += s.content
            steps += ';\n'
        form.steps.data = steps

    return render_template('add_recipe.html', title='Modify recipe', search_result=search_result, form=form)
