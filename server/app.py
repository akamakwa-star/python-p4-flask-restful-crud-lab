
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)

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
@app.route('/plants/<int:id>', methods=['PUT'])
def update_plant(id):
    plant = db.session.get(Plant, id)  # ✅ use session.get() instead of Plant.query.get()
    if not plant:
        return jsonify({'error': 'Plant not found'}), 404
    data = request.get_json()
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    db.session.commit()
    return jsonify({'id': plant.id, 'name': plant.name, 'is_in_stock': plant.is_in_stock})

if __name__ == "__main__":
    app.run(debug=True)
