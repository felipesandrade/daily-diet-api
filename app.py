from flask import Flask, request, jsonify
from database import db
from models.meal import Meal
from models.user import User
from datetime import datetime
from flask_migrate import Migrate
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

# Implementing Migrate to modify your tables and preserve data
migrate = Migrate(app, db)

db.init_app(app)  

@app.route('/meal', methods=['POST'])
def create_meal():
    data = request.json

    if 'name'in data:
        if not isinstance(data.get("name"), str) or not data.get("name").strip():
            return jsonify({"erro": "Nome inválido."}), 400
        name = data.get("name").strip()
    if 'description' in data:
        if not isinstance(data.get("description"), str) or not data.get("description").strip():
            return jsonify({"erro": "Descrição inválida."}), 400
        description = data.get("description").strip()
    if 'date_time' in data:
        date_time = data.get("date_time")
        try:
            formatted_datetime = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        except ValueError: 
            return jsonify({"erro": "Data e hora inválidos."}), 400
    if 'on_diet' in data:
        on_diet = data.get("on_diet") if data.get("on_diet") else False
        if not isinstance(on_diet, bool):
            return jsonify({"erro": "Na dieta inválido."}), 400

    meal = Meal(name=name, description=description, date_time=formatted_datetime, on_diet=on_diet)
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Refeição criada com sucesso."}), 201

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

@app.route('/meal/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if not meal:
        return jsonify({"message": "Refeição não econtrada."}), 404
        
    data = request.json

    if 'name' in data:
        if not isinstance(data.get("name"), str) or not data.get("name").strip():
            return jsonify({"erro": "Nome inválido."}), 400
        meal.name = data.get("name").strip()

    if 'description' in data:
        if not isinstance(data.get("description"), str) or not data.get("description").strip():
            return jsonify({"erro": "Descrição inválida."}), 400
        meal.description = data.get("description").strip()
    if 'date_time' in data:
        date_time = data.get("date_time")
        try:
            formatted_datetime = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"erro": "Data e hora inválidos."}), 400
        meal.date_time = formatted_datetime
    if 'on_diet' in data:
        on_diet = data.get("on_diet")
        if not isinstance(on_diet, bool):
            return jsonify({"erro": "Na diera inválida."}), 400
        meal.on_diet = on_diet

    db.session.commit()
    return jsonify({"message": "Refeição alterada com sucesso."}), 200

@app.route('/meal/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição deletada com sucesso."})
    return jsonify({"message": "Refeição não encontrada."})

@app.route('/', methods=['GET'])
def index():
    return "Daily Diet API"

if __name__ == "__main__":
    app.run(debug=True)