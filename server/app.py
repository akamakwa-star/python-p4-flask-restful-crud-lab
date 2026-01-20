
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables inside app context
with app.app_context():
    db.create_all()

# GET plant by ID (SQLAlchemy 2.0-compliant)
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = db.session.get(Plant, id)  # ✅ use session.get() instead of Plant.query.get()
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    return jsonify({'id': plant.id, 'name': plant.name, 'is_in_stock': plant.is_in_stock})

# UPDATE plant by ID (SQLAlchemy 2.0-compliant)
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = db.session.get(Plant, id)  # ✅ use session.get() instead of Plant.query.get()
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    data = request.get_json()
    for attr in ['name', 'image', 'price', 'is_in_stock']:
        if attr in data:
            setattr(plant, attr, data[attr])
    db.session.commit()
    return jsonify({'id': plant.id, 'name': plant.name, 'image': plant.image, 'price': plant.price, 'is_in_stock': plant.is_in_stock})

# DELETE plant by ID
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    db.session.delete(plant)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
