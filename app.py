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

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user_name = data.get("user_name")
    password = data.get("password")

    if user_name and password:
        user = User.query.filter_by(user_name=user_name).first()

        if not user:
            if 'user_name' in data:
                if not isinstance(user_name, str) and not user_name.strip():
                    return jsonify({"erro": "Usuário inválido."}), 400
                user_name = user_name.strip()
            if 'password' in data:
                if not isinstance(password, str) and not password.strip():
                    return jsonify({"erro": "Password inválida."}), 400
                password = password.strip()

            user = User(user_name=user_name, password=password, role="user")
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Usuário criado com sucesso."}), 201
        
        return jsonify({"message": "Usuário já cadastrado."}), 404
    
    return jsonify({"message": "Dados inválidos."}), 400

@app.route('/meal', methods=['POST'])
def create_meal():
    data = request.json
    meal_name = data.get("meal_name")
    meal_description = data.get("meal_description")
    meal_date_time = data.get("meal_date_time")
    meal_on_diet = data.get("meal_on_diet")

    if meal_name and meal_description and meal_date_time and meal_on_diet:

        if 'meal_name'in data:
            if not isinstance(meal_name, str) or not meal_name.strip():
                return jsonify({"erro": "Nome inválido."}), 400
            meal_name = meal_name.strip()
        if 'meal_description' in data:
            if not isinstance(meal_description, str) or not meal_description.strip():
                return jsonify({"erro": "Descrição inválida."}), 400
            meal_description = meal_description.strip()
        if 'meal_date_time' in data:
            try:
                formatted_meal_date_time = datetime.strptime(meal_date_time, "%Y-%m-%d %H:%M:%S")
            except ValueError: 
                return jsonify({"erro": "Data e hora inválidos."}), 400
        if 'meal_on_diet' in data:
            if not isinstance(meal_on_diet, bool):
                return jsonify({"erro": "Refeição na dieta inválido."}), 400

        meal = Meal(meal_name=meal_name, meal_description=meal_description, meal_date_time=formatted_meal_date_time, meal_on_diet=meal_on_diet)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Refeição criada com sucesso."}), 201

    return jsonify({"message": "Dados inválidos."}), 400

@app.route('/meal', methods=['GET'])
def get_meals():
    meals = Meal.query.all()

    if meals:
        meals_list = []
        for meal in meals:
            formatted_meal_date_time = meal.meal_date_time.strftime("%Y-%m-%d %H:%M:%S")
            meals_list.append({
                "id": meal.id,
                "meal_name": meal.meal_name,
                "meal_description": meal.meal_description,
                "meal_date_time": formatted_meal_date_time,
                "meal_on_diet": meal.meal_on_diet
            })
        return jsonify(meals_list), 200
    return jsonify({"message": "Nenhuma refeição encontrada."}), 400

@app.route('/meal/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal:
        formatted_meal_date_time = meal.meal_date_time.strftime("%Y-%m-%d %H:%M:%S")
        meal_data = {
            "id": meal.id,
            "meal_name": meal.meal_name,
            "meal_description": meal.meal_description,
            "meal_date_time": formatted_meal_date_time,
            "meal_on_diet": meal.meal_on_diet
        }
        return jsonify(meal_data), 200
    return jsonify({"message": "Refeição não encontrada."}), 404

@app.route('/meal/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if not meal:
        return jsonify({"message": "Refeição não econtrada."}), 404
        
    data = request.json
    meal_name = data.get("meal_name")
    meal_description = data.get("meal_description")
    meal_date_time = data.get("meal_date_time")
    meal_on_diet = data.get("meal_on_diet")


    if 'meal_name' in data:
        if not isinstance(meal_name, str) or not meal_name.strip():
            return jsonify({"erro": "Nome inválido."}), 400
        meal.meal_name = meal_name.strip()

    if 'meal_description' in data:
        if not isinstance(meal_description, str) or not meal_description.strip():
            return jsonify({"erro": "Descrição inválida."}), 400
        meal.meal_description = meal_description.strip()
    if 'meal_date_time' in data:
        try:
            formatted_meal_date_time = datetime.strptime(meal_date_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"erro": "Data e hora inválidos."}), 400
        meal.meal_date_time = formatted_meal_date_time
    if 'meal_on_diet' in data:
        if not isinstance(meal_on_diet, bool):
            return jsonify({"erro": "Na diera inválida."}), 400
        meal.meal_on_diet = meal_on_diet

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