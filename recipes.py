from app import create_app, db
from app.models import User, Recipe, DishType, Ingredient


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Recipe': Recipe, 'DishType': DishType, 'Ingredient': Ingredient}
