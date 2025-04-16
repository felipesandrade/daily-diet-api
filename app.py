from flask import Flask, request, jsonify
from database import db
from models.meal import Meal
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'

db.init_app(app)  

@app.route('/meal', methods=['PUT'])
def create_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    date_time = data.get("date_time")
    on_diet = data.get("on_diet")

    if name and description and date_time:
        try:
            meal = Meal(name=name, description=description, date_time=date_time, on_diet=on_diet)
            db.session.add(meal)
            db.session.commit()
            return jsonify({"message": "Refeição criada com sucesso."}), 201
        except Exception as e:
            return jsonify({"message": "Erro ao criar a refeição."}), 500   
    return jsonify({"message": "Dados inválidos."}), 400

@app.route('/meal', methods=['GET'])
def get_meals():
    meals = Meal.query.all()

    if meals:
        meals_list = []
        for meal in meals:
            formatted_datetime = meal.date_time.strftime("%Y-%m-%d %H:%M:%S")
            meals_list.append({
                "id": meal.id,
                "name": meal.name,
                "description": meal.description,
                "date_time": formatted_datetime,
                "on_diet": meal.on_diet
            })
        return jsonify(meals_list), 200
    return jsonify({"message": "Nenhuma refeição encontrada."}), 400

@app.route('/meal/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal:
        formatted_datetime = meal.date_time.strftime("%Y-%m-%d %H:%M:%S")
        meal_data = {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date_time": formatted_datetime,
            "on_diet": meal.on_diet
        }
        return jsonify(meal_data), 200
    return jsonify({"message": "Refeição não encontrada."}), 404
    
@app.route('/', methods=['GET'])
def index():
    return "Daily Diet API"

if __name__ == "__main__":
    app.run(debug=True)