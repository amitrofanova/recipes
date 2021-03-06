from flask import render_template, flash, redirect, url_for, request, send_from_directory, abort
from flask_login import current_user, login_required, login_user
from app import db
from app.main.forms import EditProfileForm, NewRecipeForm, SearchRecipeForm, DeleteRecipeForm, AddIdeaForm, \
    AddDishTypeForm
from app.models import User, Recipe, DishType, Ingredient, Step, Idea, RecipeImage
from app.main import bp
import os


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return show_index()


def show_index():
    recipes = current_user.recipes
    type_ids = []
    types = []

    for r in recipes:
        if r.dish_type_id not in type_ids:
            type_ids.append(r.dish_type_id)
            type = DishType.query.filter_by(id=r.dish_type_id).first()
            types.append(type)

    return render_template('index.html', title='Home', dish_types=types)


@bp.route('/demo', methods=['GET'])
def demo_index():
    user = User.query.filter_by(username='demo').first()
    if user is None:
        abort(401)

    login_user(user, remember=True)
    return show_index()


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


@bp.route('/recipes', defaults={'dish_type_id': None})
@bp.route('/recipes/<int:dish_type_id>')
@login_required
def recipes(dish_type_id):
    if dish_type_id:
        recipes = Recipe.query.filter_by(user_id=current_user.id).filter_by(dish_type_id=dish_type_id)
    else:
        recipes = Recipe.query.filter_by(user_id=current_user.id)

    return render_template('recipes.html', recipes=recipes)


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
        lines = form.ingredients.data.splitlines()
        for line in lines:
            line = line.strip()
            if line != '':
                ingredients.append(line)
        for i in ingredients:
            ingredient = Ingredient(name=i, recipe=recipe)
            db.session.add(ingredient)

        steps = []
        lines = form.steps.data.splitlines()
        for line in lines:
            line = line.strip()
            if line != '':
                steps.append(line)
        for i in steps:
            step = Step(content=i, recipe=recipe)
            db.session.add(step)

        db.session.commit()

        image_url = form.image_url.data
        image = RecipeImage(recipe_id=recipe.id, url=image_url)

        db.session.add(image)
        db.session.commit()

        flash('Your recipe has been saved!')
        return redirect(url_for('main.recipe', recipe_id=recipe.id))

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
        recipe_id = search_result[form_id].id
        recipe = Recipe.query.filter_by(id=recipe_id).first()

        Recipe.query.filter_by(id=recipe_id).delete()

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

        # empty current ingredients and steps
        ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()
        for i in ingredients:
            Ingredient.query.filter_by(id=i.id).delete()

        steps = Step.query.filter_by(recipe_id=recipe.id).all()
        for s in steps:
            Step.query.filter_by(id=s.id).delete()

        # collect new data
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.dish_type_id = form.dish_type.data

        if form.image_url.data != 'undefined':
            if recipe.image and recipe.image[0].url:
                image = RecipeImage.query.filter_by(recipe_id=recipe.id).first()
                image.url = form.image_url.data
            else:
                image_url = form.image_url.data
                image = RecipeImage(recipe_id=recipe.id, url=image_url)
                db.session.add(image)

        ingredients = []
        lines = form.ingredients.data.splitlines()
        for line in lines:
            line = line.strip()
            if line != '':
                ingredients.append(line)
        for i in ingredients:
            ingredient = Ingredient(name=i, recipe=recipe)
            db.session.add(ingredient)

        steps = []
        lines = form.steps.data.splitlines()
        for line in lines:
            line = line.strip()
            if line != '':
                steps.append(line)
        for i in steps:
            step = Step(content=i, recipe=recipe)
            db.session.add(step)

        db.session.commit()
        flash('Changes have been saved!')
        return redirect(url_for('main.recipe', recipe_id=recipe.id))

    elif request.method == 'GET':
        form.title.data = search_result.title
        form.description.data = search_result.description
        form.dish_type.data = search_result.dish_type_id

        if len(search_result.image):
            image_url = search_result.image[0].url
            image_preview_url = image_url.replace("upload", "upload/w_200,h_200,c_fill")
            form.image_url.data = image_preview_url

        ingredients = ''
        for i in search_result.ingredients:
            ingredients += i.name
            ingredients += '\n'
        form.ingredients.data = ingredients

        steps = ''
        for s in search_result.steps:
            steps += s.content
            steps += '\n'
        form.steps.data = steps

    return render_template('add_recipe.html', title='Modify recipe', search_result=search_result, form=form)


@bp.route('/try_new', methods=['GET', 'POST', 'DELETE'])
@login_required
def try_new():
    form = AddIdeaForm()

    if form.validate_on_submit():
        idea = Idea(user_id=current_user.id, title=form.title.data, description=form.description.data)

        db.session.add(idea)
        db.session.commit()

        flash('New idea has been saved!')
        return redirect(url_for('main.try_new'))

    if request.method == 'DELETE':
        idea_id = int(request.data)

        Idea.query.filter_by(id=idea_id).delete()
        db.session.commit()

        flash('Idea has been deleted')
        return ''

    ideas = current_user.ideas

    return render_template('try_new.html', title='Try new', form=form, ideas=ideas)


@bp.route('/add_dish_type', methods=['GET', 'POST'])
@login_required
def add_dish_type():
    types = DishType.query.all()
    form = AddDishTypeForm()

    if form.validate_on_submit():
        new_type = DishType(name=form.data['dish_type'])
        print(new_type)

        db.session.add(new_type)
        db.session.commit()

        flash('New dish type has been saved!')
        return redirect(url_for('main.add_dish_type'))

    return render_template('add_dish_type.html', title='Add dish type', form=form, types=types)


@bp.route('/favicon-32x32.png')
def favicon():
    return send_from_directory(os.path.join(bp.root_path, '../static', 'images'),
                               'favicon-32x32.png', mimetype='image/png')
